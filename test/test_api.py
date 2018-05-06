import sys, json
import pytest

def test_set_config(client, auth):
  auth.login()
  data = {
      'ngen': 2,
      'mutate_inpd':0.04,
      'selection_ind_value_step': 2,
      'elitism_percentage_start': 15,
      'elitism_percentage_up': 5,
      'gen_modulo_elitism': 90,
      'select_light': 20.0,
      'select_medium': 65.0,
  }
  with client:
    resp = client.get("/api/v1/config")
    assert resp.status_code == 200
    assert json.loads(resp.data)['ngen'] == 2000, resp.data
    resp = client.post("/api/v1/config", data=data)
    resp_data = json.loads(resp.data)
    assert resp.status_code == 200
    for k, v in data.iteritems():
      assert resp_data[k] == data[k], resp_data
    resp = client.get("/api/v1/config")
    assert resp.status_code == 200
    for k, v in data.iteritems():
      assert resp_data[k] == data[k], resp_data
    assert resp_data['ngen'] == 2, "WTF"
    resp = client.post("/api/v1/run")
    assert resp.status_code == 200, resp.data
    assert False == json.loads(resp.data)['solution_found']
    auth.logout()

@pytest.mark.parametrize(('ngen', 'mi', ), (
    (-1, -1),
    (2001, 1.01),
))
def _test_wrong_config(client, auth, ngen, mi):
  auth.login()

  with client:
    resp = client.post("/api/v1/config", data={ 'ngen': ngen } )
    assert resp.status_code == 400
    assert "limit for ngen is 1 to 2000." in resp.data

    resp = client.post("/api/v1/config", data={ 'mutate_inpd': mi } )
    assert resp.status_code == 400
    assert "limit for mutate_inpd is 0.001 to 1.0" in resp.data

    # TODO adding these limit to test. it's wrote somewhere
    #'selection_ind_value_step': config.selection_ind_value_step,
    #  'elitism_percentage_start': config.elitism_percentage_start,
    #  'elitism_percentage_up': config.elitism_percentage_up,
    #  'gen_modulo_elitism': config.gen_modulo_elitism,
    #  'select_light': config.select_light,
    #  'select_medium': config.select_medium
  auth.logout()
