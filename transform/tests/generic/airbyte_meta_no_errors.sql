{% test airbyte_meta_no_errors(model) %}

    select *
    from {{ model }}
    where _airbyte_meta::string!='{"errors":[]}'

{% endtest %}