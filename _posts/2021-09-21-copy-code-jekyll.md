---
layout: post
title: Copy code in jekyll themes
category: tactics
tags: [code, javascript, scss]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

Copy code for jekyll based themes 

<!--cut-->

* TOC
{:toc}

# Copy code for jekyll based themes

## Add to your custom scss file

```scss
// Copy code css
.copy-code-button {
  display: grid;
  grid-auto-flow: column;
  align-items: center;
  grid-column-gap: 4px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 4px 8px;
  color: #ffffff;
  background-color: #3f3f3f;
  position: absolute;
  border-radius: .4rem;
  right: 26px;

  &::before {
    content: "Copy";
  }

  &::after {
    content: "📋";
    display: block;
  }

  // This class will be toggled via JavaScript
  &.copied {
    &::before {
      content: "Copied!";
    }

    &::after {
      content: "✔️";
    }
  }
}
//END Copy code css
```

## Make these changes

### Add this to your `_layouts/post.html` or `_layouts/default.html`


 - ```<script src="/assets/js/copy-code.js"></script>```

### Create `/assets/js/copy-code.js`

```javascript
var codeBlocks = document.querySelectorAll('pre.highlight');

codeBlocks.forEach(function (codeBlock) {
  var copyButton = document.createElement('button');
  copyButton.className = 'copy-code-button';
  copyButton.type = 'button';
  copyButton.ariaLabel = 'Copy code to clipboard';

  codeBlock.prepend(copyButton);

  copyButton.addEventListener('click', function () {
    var code = codeBlock.querySelector('code').innerText.trim();
    window.navigator.clipboard.writeText(code);

    copyButton.classList.add('copied');

    setTimeout(function () {
      copyButton.classList.remove('copied');
    }, 4000);
  });
});
```
