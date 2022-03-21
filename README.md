# python-test-report

conftestで遊ぶ

```shell
poetry run pytest -vv --cache-clear --flake8 --cov=src --cov-branch --cov-report=term-missing --cov-report=xml --cov-report=html --html=report.html
```
