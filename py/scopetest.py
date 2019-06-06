import visa

config = {'ip': '10.5.97.239', 'channels': [1, 0, 0, 0], 'settings': [[.02, 0, 0, 0], [0, 0, 0, 0], 20e9, 0], 'recordLength': 3e4}
rm = visa.ResourceManager()
for n in range(3):
    try:
        scope = rm.open_resource('TCPIP::' + config["ip"] + '::INSTR', open_timeout=1000)
        failure = False
    except Exception as e:
        print(f'{n}: Cannot connect to scope, error: {e}')
        failure = True
        

print(scope.query('*IDN?'))


osc_sig = []
osc_time = []