# Renders distill-style markup in posts as static HTML at build time:
#   <d-cite key="a,b"/>     -> numbered citations, with a reference list built
#                              from the post's `bibliography` file (assets/bibliography/)
#   <d-footnote>…</d-footnote> -> numbered footnotes
# Both lists replace the <!--post-notes--> marker in the post layout.
require "bibtex"
require "citeproc"
require "csl/styles"

module PostNotes
  CITE = %r{<d-cite\s+key="([^"]+)"\s*(?:/>|>\s*</d-cite>)}
  NOTE = %r{<d-footnote>(.*?)</d-footnote>}m

  def self.references(site, file)
    path = File.join(site.source, "assets", "bibliography", file)
    bib = BibTeX.open(path, filter: :latex)
    cp = CiteProc::Processor.new(style: "apa", format: "html", locale: "en-US")
    cp.import(bib.to_citeproc)
    cp
  end

  def self.render(post)
    html = post.output
    return unless html.include?("<!--post-notes-->")

    order = []
    cp = post.data["bibliography"] && references(post.site, post.data["bibliography"])
    html = html.gsub(CITE) do
      links = Regexp.last_match(1).split(",").map(&:strip).map do |key|
        order << key unless order.include?(key)
        n = order.index(key) + 1
        %(<a href="#ref-#{key}">#{n}</a>)
      end
      %(<span class="cite">[#{links.join(", ")}]</span>)
    end

    notes = []
    html = html.gsub(NOTE) do
      notes << Regexp.last_match(1).strip
      n = notes.size
      %(<sup class="fn"><a href="#fn-#{n}" id="fnref-#{n}">#{n}</a></sup>)
    end

    out = +""
    unless notes.empty?
      out << %(<section class="notes"><h2>Notes</h2><ol>)
      notes.each_with_index do |t, i|
        out << %(<li id="fn-#{i + 1}">#{t} <a href="#fnref-#{i + 1}" aria-label="Back to text">&#8617;</a></li>)
      end
      out << "</ol></section>"
    end
    if cp && !order.empty?
      out << %(<section class="notes refs"><h2>References</h2><ol>)
      order.each do |key|
        ref = cp.render(:bibliography, id: key).first rescue nil
        Jekyll.logger.warn("PostNotes:", "missing reference #{key} in #{post.relative_path}") unless ref
        out << %(<li id="ref-#{key}">#{ref || key}</li>)
      end
      out << "</ol></section>"
    end
    post.output = html.sub("<!--post-notes-->", out)
  end
end

Jekyll::Hooks.register(:posts, :post_render) { |post| PostNotes.render(post) }
