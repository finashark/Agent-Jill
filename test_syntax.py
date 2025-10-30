# Test cú pháp của f-string có total_trades
customer_info = {'name': 'Test'}
analysis_result = {'metrics': {'total_trades': 100}}

# Test f-string giống như trong app
test_string = f"""
Chào {customer_info.get('name', 'anh/chị')}, em thấy anh/chị có phong cách giao dịch khá tích cực với {analysis_result['metrics']['total_trades']} lệnh.
"""

print("Test thành công!")
print(test_string)