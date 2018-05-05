import sys, json
import pytest

def test_set_config(client, auth):
  auth.login()
  data = {
      'ngen': 2,
      'mutate_inpd':0.04
  }
  with client:
    resp = client.get("/api/v1/config")
    assert resp.status_code == 200
    assert json.loads(resp.data)['ngen'] == 2000, resp.data
    resp = client.post("/api/v1/config", data=data)
    assert resp.status_code == 200
    auth.logout()
@pytest.mark.parametrize(('ngen', 'mi', ), (
    (-1, -1),
    (2001, 1.01),
))
def test_wrong_config(client, auth, ngen, mi):
  auth.login()

  with client:
    resp = client.post("/api/v1/config", data={ 'ngen': ngen } )
    assert resp.status_code == 400
    assert "limit for ngen is 1 to 2000." in resp.data

    resp = client.post("/api/v1/config", data={ 'mutate_inpd': mi } )
    assert resp.status_code == 400
    assert "limit for mutate_inpd is 0.001 to 1.0" in resp.data

  auth.logout()
