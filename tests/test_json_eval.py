from _cornflakes import eval_json

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
