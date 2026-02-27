<h2 id="publications" style="margin: 2px 0px -15px;">Publications</h2>

<div class="publications">
  <ol class="bibliography">

  {%- for link in site.data.publications.main -%}
    {%- assign pdf = link.pdf | default: "" -%}
    {%- assign code = link.code | default: "" -%}
    {%- assign page = link.page | default: "" -%}
    {%- assign bibtex = link.bibtex | default: "" -%}
    {%- assign image = link.image | default: "" -%}
    {%- assign conf_short = link.conference_short | default: "" -%}

    {%- comment -%}
      Choose a safe URL for the title:
      Prefer page > pdf > none
    {%- endcomment -%}
    {%- assign title_url = "" -%}
    {%- if page != "" -%}
      {%- assign title_url = page -%}
    {%- elsif pdf != "" -%}
      {%- assign title_url = pdf -%}
    {%- endif -%}

    {%- comment -%}
      Button label for "page" link: DOI vs Project Page
    {%- endcomment -%}
    {%- assign page_label = "Project Page" -%}
    {%- if page contains "doi.org" or page contains "doi:" -%}
      {%- assign page_label = "DOI" -%}
    {%- endif -%}

    <li>
      <div class="pub-row">
        <div class="col-sm-3 abbr" style="position: relative; padding-right: 15px; padding-left: 15px;">

          {%- if image != "" -%}
            <img src="{{ image | relative_url }}"
                 class="teaser img-fluid z-depth-1"
                 style="width: 100%; height: auto; max-height: 110px; object-fit: cover;"
                 loading="lazy"
                 alt="teaser">
          {%- endif -%}

          {%- if conf_short != "" -%}
            <abbr class="badge">{{ conf_short }}</abbr>
          {%- endif -%}

        </div>

        <div class="col-sm-9" style="position: relative; padding-right: 15px; padding-left: 20px;">
          <div class="title">
            {%- if title_url != "" -%}
              <a href="{{ title_url }}" target="_blank" rel="noopener noreferrer">{{ link.title }}</a>
            {%- else -%}
              {{ link.title }}
            {%- endif -%}
          </div>

          <div class="author">{{ link.authors }}</div>
          <div class="periodical"><em>{{ link.conference }}</em></div>

          <div class="links">
            {%- if pdf != "" -%}
              <a href="{{ pdf }}" class="btn btn-sm z-depth-0" role="button"
                 target="_blank" rel="noopener noreferrer" style="font-size:12px;">PDF</a>
            {%- endif -%}

            {%- if code != "" -%}
              <a href="{{ code }}" class="btn btn-sm z-depth-0" role="button"
                 target="_blank" rel="noopener noreferrer" style="font-size:12px;">Code</a>
            {%- endif -%}

            {%- if page != "" -%}
              <a href="{{ page }}" class="btn btn-sm z-depth-0" role="button"
                 target="_blank" rel="noopener noreferrer" style="font-size:12px;">{{ page_label }}</a>
            {%- endif -%}

            {%- if bibtex != "" -%}
              <a href="{{ bibtex }}" class="btn btn-sm z-depth-0" role="button"
                 target="_blank" rel="noopener noreferrer" style="font-size:12px;">BibTeX</a>
            {%- endif -%}

            {%- if link.notes and link.notes != "" -%}
              <strong> <i style="color:#e74d3c">{{ link.notes }}</i></strong>
            {%- endif -%}

            {%- if link.others and link.others != "" -%}
              {{ link.others }}
            {%- endif -%}
          </div>
        </div>
      </div>
    </li>
    <br>

  {%- endfor -%}

  </ol>
</div>
