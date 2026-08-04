xirr last value

- Jira changes?
- client self-serve
    - need help with client alerting module
    - 
- 

- get ryugu ci changes evidenced and share



Leaving things off for today:
- Using this MR https://gitlab.com/arcesium/internal/pi/looker-projects/looker-dev-cluster/-/merge_requests/11676
- problem appears to be that liquid like below with a fully qualified view.parameter.\_parameter\_name causes the dashboard validation issue. This happens no matter which fully qualified param name I use

      , {% if 
          cash_activity.many_to_many_protection._parameter_value == "enabled"
        %}{% endif %}

- problem also appears when using other liquid without the fully qualified name like 

        {% if 
          many_to_many_protection._parameter_value == "enabled"
        %}{% endif %}

- Liquid of this form demonstrably works (as in produces the right queries), as evidenced here https://gitlab.com/arcesium/internal/fd/fd-ryugu/-/merge_requests/1374
- 
