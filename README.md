# pipeline-utils-retry

一个简单的重试工具库，为函数调用提供自动重试能力。

## 安装

```bash
pip install pipeline-utils-retry
```

## 示例

仓库中的 `examples/demo.py` 展示了两种典型用法：

- 使用 `@retry` 装饰器包装一个易出错的函数
- 使用 `retry_call` 在需要时手动触发重试

运行示例：

```bash
python examples/demo.py
```

当函数前几次失败后，日志中会看到类似 “retrying in … seconds...” 的重试提示，最终成功返回结果。
