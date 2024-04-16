-- Assert each record was extracted by Airbyte without any errors

{% test airbyte_meta_no_errors(model) %}

    select *
    from {{ model }}
    where _airbyte_meta::string!='{"errors":[]}'

{% endtest %}