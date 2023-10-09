from cornflakes import eval_json

with open("./node_cpu_seconds_total_20230912_153000.json") as f:
    data = f.read()
    print(data[1:1000])


json_chunk = """
{"status":"success","data":{"resultType":"matrix","result":[{"metric":{"__name__":"node_cpu_seconds_total","alias":"datacenteraggregation","cluster":"F10C1","cpu":"0","datacenter":"us-mkc-ga-kvm-live","instance":"onode100101.server.lan:9100","job":"clusters","mode":"idle"},"values":[[1694532600,"14179793.82"],[1694532660,"14179793.82"],[1694532720,"14179793.82"],[1694532780,"14179793.82"],[1694532840,"14180040.55"],[1694532900,"14180040.55"]]}]}}
"""
eval_json(json_chunk)

sample_json_str = """
    {
        "name": "John",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown"
        },
        "phones": [
            "+1234567890",
            "+0987654321",
            123
        ]
    }
    """

schema = eval_json(sample_json_str)
print(schema)


sample_json_not_complete_str = """
{
  "name": "John",
  "phones": []
}
"""
schema = eval_json(sample_json_not_complete_str)
print(schema)
