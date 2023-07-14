# Unit testing task

In the `app.py` file you're given an implementation of an app. It exposes an endpoint allowing users to get the maximum and minimum tempereture predicted for next few days for a given location – latitude and longitude.

The app uses Redis as a cache. Cache key are coordinates truncated to two decimal points (so `24.8608,67.0104` and `24.8612,67.0197` will result with the same key `24.86:67.01`). Each entry in the cache expires after 24h.

Your task is to:
* write unit tests for `app.py`.

Requirements:
* You **can't** (and don't need to) edit `app.py` file.
* Your tests should achieve 100% code coverage.
* Provide full working solution as a submission (we should be able to successfully run your tests with `pytest .`, without making any edits to it). Include a screenshot of how you run the tests in your submission as well.
* You don't have to test `_get_min_max_temps` or `_get_redis_client` (by convention, functions starting with `_` are private and don't need to be tested). You also shouldn't **directly** call `get_weather` in your tests. You only need to run test client and make a requests to it (the functions above will be called as an effect of this request).
* Remember to test expected behaviour – response status code, content (what value was returned) and expected calls being made.

Hints:
* Use mocking and/or patching. When patching more than one value, remember that you write down decorators in a different order than arguments in the test function, eg.:
```python
@patch(testing.app.object_to_mock_1)
@patch(testing.app.object_to_mock_2)
def test(self, mock_2, mock_1):
    # In this test mock_1 replaced app.object_to_mock_1
    # and mock_2 replaced app.object_to_mock_2.
```
* You can test if an exception is raised with [`pytest.raises(Exception)`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises). See snippet below. Then you can get the exception itself with `err.value`.
```python
with pytest.raises(SomeException) as err:
    # Run some code that raises an exception here.
```