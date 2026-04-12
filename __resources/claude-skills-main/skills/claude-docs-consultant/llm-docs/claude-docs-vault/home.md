---
created: 2025-11-05
modified: 2025-11-05
title: "null"
url: https://docs.claude.com/en/home
category: general
tags:
  - general
---

# null

export function openSearch() {
  document.getElementById("search-bar-entry").click();
}


<div className="relative w-full pt-12 pb-0">
  <div id="background-div" className="absolute inset-0" />

  <div className="text-black dark:text-white relative z-10 flex flex-col md:flex-row gap-6" style={{ maxWidth: '70rem', marginLeft: 'auto', marginRight: 'auto', paddingLeft: '1.25rem', paddingRight: '1.25rem' }}>
    <div className="flex-1 text-center">
      <div id="home-header">
        <span className="build-with">Build with Claude</span>
      </div>

      <p
        className="description-text"
        style={{
        fontWeight: '400',
        fontSize: '20px',
        maxWidth: '42rem',
        textAlign: 'center',
        margin: '0 auto 1rem auto',
      }}
      >
        Learn how to get started with the Claude Developer Platform and Claude Code.
      </p>

      <div className="flex items-center justify-center">
        <button
          type="button"
          className="w-full flex items-center text-sm leading-6 rounded-lg mt-6 py-2.5 px-4 shadow-sm text-gray-400 bg-white dark:bg-white ring-1 ring-gray-400/20 hover:ring-gray-600/25 focus:outline-primary"
          id="home-search-entry"
          style={{
        maxWidth: '32rem',
      }}
          onClick={openSearch}
        >
          <span className="ml-[-0.3rem]">Ask Claude about docs...</span>
        </button>
      </div>
    </div>
  </div>
</div>

<div style={{ maxWidth: '70rem', marginLeft: 'auto', marginRight: 'auto', paddingLeft: '1.25rem', paddingRight: '1.25rem', marginTop: '3rem' }}>
  <h2 className="description-text" style={{ fontFamily: 'Copernicus, serif', fontWeight: '300', fontSize: '28px', marginBottom: '1.5rem', textAlign: 'center' }}>
    Claude Developer Platform
  </h2>

  <div className="home-cards-custom">
    > [!info] Get started
> Make your first API call in minutes.

    > [!info] Features overview
> Explore the advanced features and capabilities now available in Claude.

    > [!info] What's new in Claude 4.5
> Discover the latest advancements in Claude 4.5 models, including Sonnet 4.5 and Haiku 4.5.

    > [!info] API reference
> Integrate and scale using our API and SDKs.

    > [!info] Claude Console
> Craft and test powerful prompts directly in your browser.

    > [!info] Release notes
> Learn about changes and new features in the Claude Developer Platform.
  </div>
</div>

<div style={{ maxWidth: '70rem', marginLeft: 'auto', marginRight: 'auto', paddingLeft: '1.25rem', paddingRight: '1.25rem', marginTop: '3rem' }}>
  <h2 className="description-text" style={{ fontFamily: 'Copernicus, serif', fontWeight: '300', fontSize: '28px', marginBottom: '1.5rem', textAlign: 'center' }}>
    Claude Code
  </h2>

  <div className="home-cards-custom">
    > [!info] Claude Code quickstart
> Get started with Claude Code.

    > [!info] Claude Code reference
> Consult the Claude Code reference documentation for details on feature implementation and configuration.

    > [!info] Claude Code changelog
> Learn about changes and new features in Claude Code.
  </div>
</div>

<div style={{ maxWidth: '70rem', marginLeft: 'auto', marginRight: 'auto', paddingLeft: '1.25rem', paddingRight: '1.25rem', marginTop: '3rem', marginBottom: '4rem' }}>
  <h2 className="description-text" style={{ fontFamily: 'Copernicus, serif', fontWeight: '300', fontSize: '28px', marginBottom: '1.5rem', textAlign: 'center' }}>
    Learning resources
  </h2>

  <div className="home-cards-custom">
    > [!info] Anthropic Courses
> Explore Anthropic's educational courses and projects.

    > [!info] Claude Cookbook
> See replicable code samples and implementations.

    > [!info] Claude Quickstarts
> Deployable applications built with our API.
  </div>
</div>

---

**Source:** [Official Documentation](https://docs.claude.com/en/home)
