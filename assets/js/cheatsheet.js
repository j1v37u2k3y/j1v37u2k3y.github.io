(function () {
  'use strict';

  // Tag mapping: normalized H1 text (lowercase) → array of tags
  var TAG_MAP = {
    'reverse shells':           ['linux', 'windows'],
    'file transfer':            ['linux', 'windows'],
    'network attacks':          ['network'],
    'vnc':                      ['network'],
    'smb':                      ['network'],
    'nfs':                      ['network'],
    'ldap':                     ['ad', 'network'],
    'ad':                       ['ad'],
    'abuse privileges':         ['windows', 'ad'],
    'remote management':        ['windows'],
    'mimikatz':                 ['credentials', 'ad'],
    'dump credentials':         ['credentials', 'ad'],
    'ntlm':                     ['credentials', 'ad'],
    'executionpolicy bypass':   ['windows'],
    'amsi bypass':              ['windows'],
    'uac bypass':               ['windows'],
    'applocker bypass':         ['windows'],
    'av bypass':                ['windows'],
    'metasploit':               ['tools'],
    'information gathering':    ['recon'],
    'ipsec':                    ['recon', 'network'],
    'discovery':                ['recon', 'network'],
    'pivoting':                 ['network'],
    'lpe':                      ['linux', 'windows'],
    'auth brute force':         ['brute-force'],
    'password brute force':     ['brute-force'],
    'dbms':                     ['web'],
    'web':                      ['web'],
    'reverse & pwn':            ['reverse'],
    'engagement':               ['recon', 'network'],
    'mindmaps':                 ['recon'],
    'sublime text':             ['tools'],
    'git':                      ['tools'],
    'docker':                   ['tools'],
    'python':                   ['tools'],
    'gpg':                      ['tools'],
    'virtualbox':               ['tools'],
    'kali':                     ['tools'],
    'unix':                     ['linux'],
    'windows':                  ['windows'],
    'ssh':                      ['linux'],
    'busybox':                  ['linux']
  };

  var ALL_TAGS = [
    'linux', 'windows', 'web', 'ad', 'network', 'credentials',
    'recon', 'brute-force', 'reverse', 'tools'
  ];

  var activeTags = [];
  var allCollapsed = false;

  // Extract heading text, ignoring anchor link children (e.g. the "#" link)
  function getHeadingText(h1) {
    var text = '';
    for (var i = 0; i < h1.childNodes.length; i++) {
      var child = h1.childNodes[i];
      if (child.nodeType === 3) { // text node
        text += child.textContent;
      }
    }
    return text.trim().toLowerCase();
  }

  function init() {
    var postContent = document.querySelector('article > .container');
    if (!postContent) return;

    wrapSections(postContent);
    buildFilterBar(postContent);
    bindCollapse();
  }

  // Wrap content between H1s into .cheatsheet-section divs
  function wrapSections(container) {
    var children = Array.prototype.slice.call(container.childNodes);
    var currentSection = null;
    var currentBody = null;

    children.forEach(function (node) {
      if (node.nodeType === 1 && node.tagName === 'H1') {
        // Create section wrapper
        currentSection = document.createElement('div');
        currentSection.className = 'cheatsheet-section';

        // Assign tags — strip anchor link text (e.g. "#") from heading
        var headingText = getHeadingText(node);
        var tags = TAG_MAP[headingText] || [];
        currentSection.setAttribute('data-tags', tags.join(','));

        // Insert section wrapper before the H1
        container.insertBefore(currentSection, node);
        currentSection.appendChild(node);

        // Create body wrapper
        currentBody = document.createElement('div');
        currentBody.className = 'cheatsheet-section-body';
        currentSection.appendChild(currentBody);
      } else if (currentBody) {
        currentBody.appendChild(node);
      }
    });
  }

  function buildFilterBar(container) {
    var bar = document.createElement('div');
    bar.className = 'cheatsheet-filter-bar';

    var label = document.createElement('span');
    label.className = 'filter-label';
    label.textContent = 'Filter:';
    bar.appendChild(label);

    ALL_TAGS.forEach(function (tag) {
      var chip = document.createElement('button');
      chip.className = 'chip';
      chip.setAttribute('data-tag', tag);
      chip.textContent = tag;
      chip.addEventListener('click', function () {
        toggleTag(tag, chip);
      });
      bar.appendChild(chip);
    });

    // Collapse/Expand all button
    var controls = document.createElement('span');
    controls.className = 'chip-controls';
    var toggleBtn = document.createElement('button');
    toggleBtn.className = 'btn-collapse-toggle';
    toggleBtn.textContent = 'Collapse All';
    toggleBtn.addEventListener('click', function () {
      allCollapsed = !allCollapsed;
      toggleBtn.textContent = allCollapsed ? 'Expand All' : 'Collapse All';
      toggleAllSections(allCollapsed);
    });
    controls.appendChild(toggleBtn);
    bar.appendChild(controls);

    container.insertBefore(bar, container.firstChild);
  }

  function toggleTag(tag, chip) {
    var idx = activeTags.indexOf(tag);
    if (idx > -1) {
      activeTags.splice(idx, 1);
      chip.classList.remove('active');
    } else {
      activeTags.push(tag);
      chip.classList.add('active');
    }
    applyFilter();
  }

  function applyFilter() {
    var sections = document.querySelectorAll('.cheatsheet-section');
    var tocNav = document.querySelector('nav[data-toggle="toc"]');

    sections.forEach(function (section) {
      if (activeTags.length === 0) {
        section.classList.remove('hidden-by-filter');
      } else {
        var sectionTags = (section.getAttribute('data-tags') || '').split(',');
        var match = activeTags.some(function (t) {
          return sectionTags.indexOf(t) > -1;
        });
        section.classList.toggle('hidden-by-filter', !match);
      }
    });

    // Sync ToC visibility
    if (tocNav) {
      var tocLinks = tocNav.querySelectorAll('a');
      tocLinks.forEach(function (link) {
        var href = link.getAttribute('href');
        if (!href || href.charAt(0) !== '#') return;
        var target = document.getElementById(href.substring(1));
        if (!target) return;

        var parentSection = target.closest('.cheatsheet-section');
        var listItem = link.closest('li');
        if (parentSection && listItem) {
          listItem.style.display = parentSection.classList.contains('hidden-by-filter') ? 'none' : '';
        }
      });
    }
  }

  function bindCollapse() {
    var headings = document.querySelectorAll('.cheatsheet-section > h1');
    headings.forEach(function (h1) {
      h1.addEventListener('click', function () {
        var body = h1.nextElementSibling;
        if (!body) return;
        var isCollapsed = body.classList.contains('collapsed');
        body.classList.toggle('collapsed', !isCollapsed);
        h1.classList.toggle('collapsed', !isCollapsed);
      });
    });
  }

  function toggleAllSections(collapse) {
    var sections = document.querySelectorAll('.cheatsheet-section');
    sections.forEach(function (section) {
      var h1 = section.querySelector('h1');
      var body = section.querySelector('.cheatsheet-section-body');
      if (h1 && body) {
        h1.classList.toggle('collapsed', collapse);
        body.classList.toggle('collapsed', collapse);
      }
    });
  }

  // Run after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
