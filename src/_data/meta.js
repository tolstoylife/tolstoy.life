export const url = process.env.URL || 'http://localhost:8080';
export const siteName = 'tolstoy.life';
export const siteDescription = 'An encyclopedic reference covering the life and works of Leo Tolstoy.';
// Extract domain from `url`
export const domain = new URL(url).hostname;
export const siteType = 'WebSite'; // schema
export const locale = 'en_EN';
export const lang = 'en';
export const skipContent = 'Skip to content';
export const author = {
  name: 'tolstoy.life',
  avatar: '',
  email: '',
  website: 'https://tolstoy.life',
  fediverse: ''
};
export const creator = {
  name: 'Johan Edlund',
  email: '',
  website: 'https://www.johanedlund.se',
  mastodon: '',
  x: ''
};
export const pathToSvgLogo = 'src/assets/svg/misc/logo.svg'; // used for favicon generation
//Color Hunt Palette f4f4f2e8e8e8bbbfca495464.png
export const themeColor = '#495464'; // used in manifest, for example primary color value
export const themeLight = '#F4F4F2'; // used for meta tag theme-color, if light colors are prefered. best use value set for light bg
export const themeDark = '#bbbfca'; // used for meta tag theme-color, if dark colors are prefered. best use value set for dark bg
export const opengraph_default = '/assets/images/template/opengraph-default.jpg'; // fallback/default meta image
export const opengraph_default_alt =
  'tolstoy.life — An encyclopedic reference covering the life and works of Leo Tolstoy.';
export const blog = {
  // RSS feed
  name: 'tolstoy.life',
  description: 'An encyclopedic reference covering the life and works of Leo Tolstoy.',
  // feed links are looped over in the head. You may add more to the array.
  feedLinks: [{
      title: 'Atom Feed',
      url: '/feed.xml',
      type: 'application/atom+xml'
    },
    {
      title: 'JSON Feed',
      url: '/feed.json',
      type: 'application/json'
    }
  ],
  // Tags
  tagSingle: 'Tag',
  tagPlural: 'Tags',
  tagMore: 'More tags:',
  // pagination
  paginationLabel: 'Articles',
  paginationPage: 'Page',
  paginationPrevious: 'Previous',
  paginationNext: 'Next',
  paginationNumbers: true
};
export const details = {
  aria: 'section controls',
  expand: 'expand all',
  collapse: 'collapse all'
};
export const dialog = {
  close: 'Close',
  next: 'Next',
  previous: 'Previous'
};
export const navigation = {
  navLabel: 'Menu',
  ariaTop: 'Main',
  ariaBottom: 'Complementary',
  ariaPlatforms: 'Platforms',
  drawerNav: true,
  subMenu: true
};
export const themeSwitch = {
  title: 'Theme',
  light: 'light',
  dark: 'dark'
};
export const greenweb = {
  // https://carbontxt.org/
  disclosures: [{
    docType: 'sustainability-page',
    url: `${url}/sustainability/`,
    domain: domain
  }],
  services: [{ domain: 'netlify.com', serviceType: 'cdn' }]
};
export const tests = {
  pa11y: {
    // keep customPaths empty if you want to test all pages
    customPaths: ['/', '/about/'],
    globalIgnore: []
  }
};
export const viewRepo = {
  // this is for the view/edit on github link. The value in the package.json will be pulled in.
  allow: true,
  infoText: 'View this page on GitHub',
  issuesPage: 'Report accessibility issues'
};
export const easteregg = false;
