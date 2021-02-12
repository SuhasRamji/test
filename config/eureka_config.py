import py_eureka_client.eureka_client as ec

port = 5000

ec.init(eureka_server="http://localhost:8761/eureka",
                   app_name="POC",
                   instance_port=port)