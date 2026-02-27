<h2 id="publications" style="margin: 2px 0px -15px;">Publications</h2>

{%- assign pubs = site.data.publications.main -%}
{%- assign selected_pubs = pubs | where: "selected", true -%}

{%- comment -%}
  If you mark some items as selected: true in _data/publications.yml,
  we show Selected first, and the rest under "More".
{%- endcomment -%}

{%- if selected_pubs.size > 0 -%}
  <div class="publications">
    <h3 style="margin-top: 12px;">Selected</h3>
    <ol class="bibliography" style="padding-left: 18px;">
      {%- for link in selected_pubs -%}
        {% include_relative _includes/pub_item.html %}
      {%- endfor -%}
    </ol>

    <details style="margin-top: 10px;">
      <summary style="cursor: pointer; font-weight: 600;">More publications</summary>
      <ol class="bibliography" style="padding-left: 18px; margin-top: 10px;">
        {%- for link in pubs -%}
          {%- unless link.selected == true -%}
            {% include_relative _includes/pub_item.html %}
          {%- endunless -%}
        {%- endfor -%}
      </ol>
    </details>
  </div>

{%- else -%}

  <div class="publications">
    <ol class="bibliography" style="padding-left: 18px;">
      {%- for link in pubs -%}
        {% include_relative _includes/pub_item.html %}
      {%- endfor -%}
    </ol>
  </div>

{%- endif -%}
