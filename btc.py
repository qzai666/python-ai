from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # 或 Firefox/Edge
driver.get("https://web3.okx.com/zh-hans/explorer/bitcoin/token/brc20/457175")

# 方法 2A：直接查找所有带 data 属性的元素
data_elements = driver.find_elements(By.CSS_SELECTOR, "[data-original]")  # 所有含 data 属性的元素
data_values = [element.get_attribute("data-original") for element in data_elements]

# 方法 2B：精确查找表格某一列的 data 值
# 假设表格第 2 列的 <span> 标签有 data 属性
rows = driver.find_elements(By.CSS_SELECTOR, "table tr")  # 所有行
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")  # 所有列
    if len(columns) >= 2:  # 确保至少有 2 列
        target_column = columns[1]  # 第 2 列
        data_spans = target_column.find_elements(By.CSS_SELECTOR, "span[data-original]")
        for span in data_spans:
            print(span.get_attribute("data-original"))

print("所有 data 值:", data_values)
driver.quit()