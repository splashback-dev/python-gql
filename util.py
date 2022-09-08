from typing import Any


def gql_flatten(key: str, data: Any) -> Any:
    if isinstance(data, list):
        result = []
        for d in data:
            value = gql_flatten(key, d)
            if isinstance(value, list):
                result += value
            else:
                result.append(value)
        return result

    if isinstance(data, dict):
        result = {}
        list_key = None
        for k, list_v in data.items():
            result_k = f'{key}.{k}'
            result_v = gql_flatten(k, list_v)

            if isinstance(result_v, list):
                list_key = result_k
                result[result_k] = result_v
            elif isinstance(result_v, dict):
                result = {**result, **result_v}
            else:
                result[result_k] = result_v

        if list_key is None:
            return result

        result_list = []
        list_value = result[list_key]
        for list_v in list_value:
            if isinstance(list_v, dict):
                result_v = {**result, **list_v}
                del result_v[list_key]
                result_list.append(result_v)
            else:
                result_list.append({
                    **result,
                    list_key: list_v
                })
        return result_list

    else:
        return data
