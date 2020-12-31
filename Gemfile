# frozen_string_literal: true

source "https://rubygems.org"

group :jekyll_plugins do
  gem "github-pages"
  gem "jekyll-sitemap"
  gem "jemoji"
  gem "jekyll", ">= 3.5", "< 5.0"
  gem "jekyll-feed", "~> 0.9"
  gem "jekyll-seo-tag", "~> 2.1"
  gem "jekyll-paginate", "~> 1.1"
  gem "jekyll-redirect-from", "~> 0.12"
  gem "jekyll-toc"
  gem "jekyll-twitter-plugin"
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.0" if Gem.win_platform?

gem "jekyll", ENV["JEKYLL_VERSION"] if ENV["JEKYLL_VERSION"]
gem "kramdown-parser-gfm" if ENV["JEKYLL_VERSION"] == "~> 3.9"
