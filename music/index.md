---
layout: default
---

# Free music

{% for file in site.static_files %}
    {% if file.path contains '/assets/audio' %}

## {{ file.basename }}
<audio preload="none" controls>
    <source src="{{ file.path }}">
</audio>

    {% endif %}
{% endfor %}
