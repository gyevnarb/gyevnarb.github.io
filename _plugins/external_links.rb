require "uri"

# Open links that leave the site in a new tab.
# Adds target="_blank" rel="noopener" to every <a href="http(s)://..."> in
# rendered HTML whose host is not the site's own, unless a target is already set.
module ExternalLinks
  ANCHOR = /<a\s[^>]*>/i
  HREF = /\shref\s*=\s*["']\s*(?:https?:)?\/\/([^\/"'?#:]+)/i

  def self.process(doc)
    return unless doc.output_ext == ".html" && doc.output
    own_host = URI(doc.site.config["url"].to_s).host rescue nil
    doc.output = doc.output.gsub(ANCHOR) do |tag|
      host = tag[HREF, 1]
      next tag if host.nil? || tag =~ /\starget\s*=/i
      next tag if own_host && host.downcase.sub(/\Awww\./, "") == own_host.downcase.sub(/\Awww\./, "")
      tag.sub(/>\z/, ' target="_blank" rel="noopener">')
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  ExternalLinks.process(doc)
end
