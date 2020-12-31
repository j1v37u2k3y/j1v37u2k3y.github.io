# frozen_string_literal: true

source "https://rubygems.org"

gem 'jekyll'

group :jekyll_plugins do
  gem "github-pages"
  gem "jekyll-sitemap"
  gem "jemoji"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
  gem "jekyll-redirect-from"
  gem "jekyll-toc"
  gem "jekyll-twitter-plugin"
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.0" if Gem.win_platform?

gem "kramdown-parser-gfm" if ENV["JEKYLL_VERSION"] == "~> 3.9"
