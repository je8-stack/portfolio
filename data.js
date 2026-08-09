/**
 * Portfolio Data Management
 * Centralized data source with helper methods for portfolio content.
 * Works in both browser (window) and Node.js (module) environments.
 */

// Default data (can be loaded from data.json at runtime)
const DEFAULT_DATA = {
  lastUpdated: "2026-08-09T19:40:00",

  profile: {
    name: "Alward Jevon Soeminto Putra",
    title: "Product Manager",
    email: "alwardjevon@yahoo.com",
    phone: "+62-811-3498-134",
    website: "https://je8-stack.github.io/portfolio/",
    location: "Depok, Indonesia",
    linkedin: ""
  },

  projects: [
    {
      id: "product-intelligence-platform",
      title: "Product Intelligence Platform",
      category: "Product Intelligence",
      year: "2026",
      featured: true,
      summary: "Built an AI-powered product intelligence platform that transformed fragmented product data into faster decisions.",
      challenge: "Product decisions relied on fragmented data and manual competitive tracking.",
      solution: "Centralized AI platform for unified product and market intelligence.",
      impact: "Reduced decision time and improved portfolio visibility across multiple product lines.",
      stack: ["Product Intelligence", "AI", "Market Research", "Competitive Analysis"],
      image: "project-tkdn.jpg"
    },
    {
      id: "tender-intelligence-platform",
      title: "Tender Intelligence Platform",
      category: "Business Intelligence",
      year: "2026",
      featured: false,
      summary: "AI-powered tender intelligence that transformed government procurement data into actionable opportunities.",
      challenge: "Government procurement scattered across millions of RUP records.",
      solution: "Automated platform analyzing INAPROC data with intelligent product matching.",
      impact: "Accelerated product recommendations for B2G opportunities.",
      stack: ["AI Tender Intelligence", "Procurement Analytics", "Product Matching", "Automated Insights"],
      image: "project-keyaccount.jpg"
    },
    {
      id: "inventory-intelligence-platform",
      title: "Inventory Intelligence Platform",
      category: "Operations Intelligence",
      year: "2026",
      featured: false,
      summary: "Automated decision support for inventory risks and operational recommendations.",
      challenge: "Manual monitoring of stockouts, last-buy products, and lifecycle changes.",
      solution: "Real-time risk identification with prioritized action recommendations.",
      impact: "Proactive inventory management and improved distributor readiness.",
      stack: ["Inventory Intelligence", "Automated Analytics", "Decision Support", "Operational Risk"],
      image: "project-lean.jpg"
    }
  ],

  career: [
    {
      id: "pm-axioo",
      title: "Product Manager",
      company: "PT Tera Data Indonusa · Axioo",
      period: "Aug 2021 — Present",
      current: true,
      description: "Market research for B2G, vendor/OEM sourcing, lifecycle decisions aligned with company goals and profitability.",
      tags: ["Product Roadmap", "Market Research", "TKDN", "Vendor Management", "Dealer Gathering"]
    },
    {
      id: "account-manager",
      title: "Account Manager",
      company: "PT Tera Data Indonusa · Axioo",
      period: "Sep 2018 — Jan 2020",
      current: false,
      description: "Build relationships with banking stakeholders across IT, procurement, and operations. Secured 3 banking tenders totaling USD 1,500.",
      tags: ["Key Account", "Banking Tenders", "Stakeholder Management"]
    }
  ],

  education: [
    {
      id: "msc-leeds",
      degree: "MSc. International Business",
      school: "University of Leeds · United Kingdom",
      period: "Aug 2022 — Present",
      description: "Thesis on Commonwealth principle influencing inward FDI among ASEAN members. Award: MSc Contribution Prize.",
      tags: ["International Business", "FDI & Trade", "Research"]
    },
    {
      id: "bba-jilin",
      degree: "BBA. International Business",
      school: "Jilin University · Lambton College · China",
      period: "Aug 2015 — Aug 2018",
      description: "Undergraduate foundation in international business. Award: Dean's Honour Award.",
      tags: ["Business Administration", "International Trade"]
    }
  ],

  expertise: [
    {
      id: "product-strategy",
      title: "Product Strategy",
      description: "Roadmap planning, portfolio prioritization, and TKDN alignment for B2G growth."
    },
    {
      id: "market-intelligence",
      title: "Market Data Intelligence",
      description: "Transforming market signals into prioritized product and go-to-market decisions."
    },
    {
      id: "product-management",
      title: "Product Management",
      description: "Lifecycle management, vendor sourcing, and inventory strategy tied to profitability."
    },
    {
      id: "sales-enablement",
      title: "Sales Enablement",
      description: "Strategic storytelling that accelerates deal cycles and strengthens accounts."
    },
    {
      id: "business-process",
      title: "Business Process",
      description: "Streamlining workflows and improving production cost efficiency."
    },
    {
      id: "vendor-negotiation",
      title: "Vendor Negotiation",
      description: "Sourcing hardware, platforms, and OEM partners with strong commercial terms."
    }
  ],

  additional: {
    languages: ["Bahasa", "English", "Mandarin"],
    certifications: ["IELTS 6.5"],
    activities: [
      "Perhimpunan Pelajar Indonesia di Tiongkok (2015-2018)",
      "Perhimpunan Pelajar Indonesia di Inggris Raya (2018-2019)"
    ]
  }
};

/**
 * Portfolio Manager Class
 * Manages portfolio data with query and update methods.
 */
class PortfolioManager {
  constructor(data = DEFAULT_DATA) {
    this._data = data;
  }

  // --- Getters ---
  get profile() { return this._data.profile; }
  get projects() { return this._data.projects; }
  get career() { return this._data.career; }
  get education() { return this._data.education; }
  get expertise() { return this._data.expertise; }
  get additional() { return this._data.additional; }
  get lastUpdated() { return this._data.lastUpdated; }

  // --- Query Methods ---
  getProjectById(id) {
    return this._data.projects.find(p => p.id === id) || null;
  }

  getFeaturedProject() {
    return this._data.projects.find(p => p.featured) || this._data.projects[0];
  }

  getProjectsByCategory(category) {
    return this._data.projects.filter(p => p.category === category);
  }

  getCareerById(id) {
    return this._data.career.find(c => c.id === id) || null;
  }

  getCurrentRole() {
    return this._data.career.find(c => c.current) || null;
  }

  getEducationById(id) {
    return this._data.education.find(e => e.id === id) || null;
  }

  getExpertiseById(id) {
    return this._data.expertise.find(e => e.id === id) || null;
  }

  // --- Update Methods ---
  updateProfile(updates) {
    this._data.profile = { ...this._data.profile, ...updates };
    return this;
  }

  addProject(project) {
    this._data.projects.unshift(project);
    return this;
  }

  updateProject(id, updates) {
    const project = this.getProjectById(id);
    if (project) {
      Object.assign(project, updates);
    }
    return this;
  }

  updateFromJSON(jsonData) {
    this._data = { ...this._data, ...jsonData };
    this._data.lastUpdated = new Date().toISOString();
    return this;
  }

  // --- Export ---
  toJSON() {
    return JSON.parse(JSON.stringify(this._data));
  }

  // --- Stats ---
  getCareerYears() {
    const earliest = this._data.career.reduce((min, role) => {
      const match = role.period.match(/(\d{4})/);
      return match ? Math.min(min, parseInt(match[1])) : min;
    }, Infinity);
    return earliest < 9999 ? new Date().getFullYear() - earliest + 1 : 0;
  }

  getCounts() {
    return {
      projects: this._data.projects.length,
      experience: this._data.career.length,
      education: this._data.education.length,
      expertise: this._data.expertise.length
    };
  }
}

// Browser export
if (typeof window !== 'undefined') {
  window.PortfolioManager = PortfolioManager;
  window.portfolio = new PortfolioManager();
}

// Node.js export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PortfolioManager, DEFAULT_DATA };
}
