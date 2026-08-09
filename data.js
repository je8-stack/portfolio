/**
 * Portfolio Data Management
 * Centralized data source for portfolio content
 */

const PortfolioData = {
  // Profile Information
  profile: {
    name: "Alward Jevon Soeminto Putra",
    title: "Product Manager",
    email: "alwardjevon@yahoo.com",
    phone: "+62-811-3498-134",
    website: "https://je8-stack.github.io/portfolio/",
    location: "Depok, Indonesia",
    summary: [
      "AI-driven Product Manager with experience in Account Management and Product Strategy since 2021.",
      "Specialized in product intelligence, market opportunity analysis, portfolio management, and B2G strategy.",
      "Transforming customer insight into data-driven product that strengthen profitability and portfolio performance."
    ].join(" ")
  },

  // Projects Data
  projects: [
    {
      id: "product-intelligence-platform",
      title: "Product Intelligence Platform",
      category: "Product Intelligence",
      year: "2026",
      description: "Built an AI-powered product intelligence platform that accelerated product decisions, strengthened competitive positioning, and supported profitable growth across multiple product lines.",
      features: [
        "Market data aggregation & competitive analysis",
        "AI-driven insights for faster decisions",
        "Supports Notebook, AIO, Smartboard & Videotron"
      ],
      tags: ["Product Intelligence", "AI", "Market Research", "Competitive Analysis"],
      link: "https://intel.axioo/product",
      image: "project-tkdn.jpg"
    },
    {
      id: "tender-intelligence-platform",
      title: "Tender Intelligence Platform",
      category: "Business Intelligence",
      year: "2026",
      description: "Built an AI-powered tender intelligence platform that transformed government procurement data into actionable product opportunities, enabling faster opportunity identification and smarter portfolio decisions.",
      features: [
        "Procurement data analysis",
        "Product matching", 
        "Automated insights"
      ],
      tags: ["AI Tender Intelligence", "Procurement Analytics", "Product Matching", "Automated Insights"],
      link: "https://tender.axioo/intel",
      image: "project-keyaccount.jpg"
    },
    {
      id: "inventory-intelligence-platform",
      title: "Inventory Intelligence Platform",
      category: "Operations Intelligence",
      year: "2026",
      description: "Proactive inventory management, faster operational decisions, and improved distributor readiness.",
      features: [
        "Inventory risk monitoring",
        "Operational decision support",
        "Distributor readiness tracking"
      ],
      tags: ["Inventory Intelligence", "Automated Analytics", "Decision Support", "Operational Risk"],
      link: "https://inventory.axioo/intel",
      image: "project-lean.jpg"
    }
  ],

  // Expertise Areas
  expertise: [
    {
      id: "product-strategy",
      title: "Product Strategy",
      description: "Roadmap planning, portfolio prioritization, and TKDN alignment to drive B2G product growth and market expansion.",
      icon: "strategy"
    },
    {
      id: "market-intelligence",
      title: "Market Data Intelligence",
      description: "Transforming market signals, dealer insights, and competitive trends into prioritized product and go-to-market decisions.",
      icon: "intelligence"
    },
    {
      id: "product-management",
      title: "Product Management",
      description: "Lifecycle management, vendor sourcing, OEM alignment, and inventory strategy tied to profitability.",
      icon: "management"
    },
    {
      id: "sales-enablement",
      title: "Sales Enablement",
      description: "Presentation and strategic storytelling that accelerates deal cycles and strengthens banking and government accounts.",
      icon: "sales"
    },
    {
      id: "business-process",
      title: "Business Process",
      description: "Streamlining operational workflows, improving production cost efficiency, and driving portfolio visibility.",
      icon: "process"
    },
    {
      id: "vendor-negotiation",
      title: "Vendor Negotiation",
      description: "Identifying and sourcing hardware, digital platforms, and OEM partners with strong commercial terms and delivery reliability.",
      icon: "vendor"
    }
  ],

  // Career Timeline
  career: [
    {
      id: "pm-axioo",
      title: "Product Manager",
      company: "PT Tera Data Indonusa · Axioo",
      period: "Aug 2021 — Present",
      description: "Perform Market Research for B2G to identify customer needs, trends, and opportunities through Dealer Gathering. Identify, source, and negotiate with vendors for hardware components, digital platforms, and OEM services. Align lifecycle decisions with company goals, inventory strategy, and profitability.",
      tags: ["Product Roadmap", "Market Research", "TKDN", "Vendor Management", "Dealer Gathering"],
      current: true
    },
    {
      id: "account-manager",
      title: "Account Manager",
      company: "PT Tera Data Indonusa · Axioo",
      period: "Sep 2018 — Jan 2020",
      description: "Build and maintain strong relationships with banking stakeholders across IT, procurement, and operations teams. Successfully secured 3 banking tenders totaling USD 1,500, showcasing strategic sales ability and market alignment.",
      tags: ["Key Account", "Banking Tenders", "Stakeholder Management"]
    }
  ],

  // Education
  education: [
    {
      id: "msc-leeds",
      title: "MSc. International Business",
      school: "University of Leeds · United Kingdom",
      period: "Aug 2022 — Present",
      description: "Thesis on the role of the Commonwealth principle in influencing inward FDI flows among ASEAN members. Award: MSc Contribution Prize.",
      tags: ["International Business", "FDI & Trade", "Research"]
    },
    {
      id: "bba-jilin",
      title: "BBA. International Business",
      school: "Jilin University · Lambton College · China",
      period: "Aug 2015 — Aug 2018",
      description: "Undergraduate foundation in international business. Award: Dean's Honour Award.",
      tags: ["Business Administration", "International Trade"]
    }
  ],

  // Additional Information
  additional: {
    languages: ["Bahasa", "English", "Mandarin"],
    certifications: ["IELTS 6.5"],
    activities: [
      "Perhimpunan Pelajar Indonesia di Tiongkok (2015-2018)",
      "Perhimpunan Pelajar Indonesia di Inggris Raya (2018-2019)"
    ]
  },

  // Helper Methods
  getProjectById(id) {
    return this.projects.find(p => p.id === id);
  },

  getCareerById(id) {
    return this.career.find(c => c.id === id);
  },

  getExpertiseById(id) {
    return this.expertise.find(e => e.id === id);
  },

  // Update from CV data
  updateFromCV(cvData) {
    Object.assign(this.profile, cvData.profile || {});
    this.projects = cvData.projects || this.projects;
    this.expertise = cvData.expertise || this.expertise;
    this.career = cvData.career || this.career;
    this.education = cvData.education || this.education;
    this.additional = cvData.additional || this.additional;
    return this;
  },

  // Export to JSON
  toJSON() {
    return {
      profile: this.profile,
      projects: this.projects,
      expertise: this.expertise,
      career: this.career,
      education: this.education,
      additional: this.additional,
      lastUpdated: new Date().toISOString()
    };
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PortfolioData;
} else if (typeof window !== 'undefined') {
  window.PortfolioData = PortfolioData;
}