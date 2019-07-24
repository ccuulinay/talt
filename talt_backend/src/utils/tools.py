
def update_dictionary_value(src_dict, tgt_dict):
    from collections.abc import MutableMapping
    import copy
    for key, src_value in src_dict.items():
        if key in tgt_dict.keys():
            tgt_value = tgt_dict[key]
            if isinstance(src_value, MutableMapping):
                if isinstance(tgt_value, MutableMapping):
                    update_dictionary_value(src_value, tgt_value)
                else:
                    tgt_dict[key] = copy.deepcopy(src_value)
            else:
                tgt_dict[key] = copy.deepcopy(src_value)

        else:
            tgt_dict[key] = copy.deepcopy(src_value)

