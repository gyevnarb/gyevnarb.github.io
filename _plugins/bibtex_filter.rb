# Strips site-only fields (see `filtered_bibtex_keywords` in _config.yml) and
# equal-contribution markers from the BibTeX shown on publication entries.
module Jekyll
  module HideCustomBibtex
    def hide_custom_bibtex(input)
      keys = @context.registers[:site].config["filtered_bibtex_keywords"] || []
      keys.each { |k| input = input.gsub(/^\s*#{k}\s*=\s*\{.*\},?\s*$\n?/, "") }
      input.gsub(/^\s*author\s*=.*$/) { |line| line.delete("*") }
    end
  end
end

Liquid::Template.register_filter(Jekyll::HideCustomBibtex)
