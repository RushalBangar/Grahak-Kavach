import re

def update_officer_dashboard():
    with open('frontend/officer-dashboard.html', 'r', encoding='utf-8') as f:
        old_content = f.read()

    new_content = """<!DOCTYPE html>
<html class="light" lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grahak Kavach - Officer Dashboard</title>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-tertiary": "#ffffff", "secondary-fixed": "#d5e3fd", "on-background": "#1b1b1d",
                        "on-tertiary-fixed": "#191c1e", "error-container": "#ffdad6", "on-tertiary-container": "#818486",
                        "on-primary-container": "#7c839b", "inverse-surface": "#303032", "tertiary": "#000000",
                        "surface-container-lowest": "#ffffff", "on-error": "#ffffff", "surface-container-highest": "#e4e2e4",
                        "primary": "#000000", "tertiary-fixed-dim": "#c4c7c9", "inverse-primary": "#bec6e0",
                        "primary-fixed-dim": "#bec6e0", "secondary-fixed-dim": "#b9c7e0", "secondary": "#515f74",
                        "surface-variant": "#e4e2e4", "tertiary-fixed": "#e0e3e5", "on-surface": "#1b1b1d",
                        "on-secondary": "#ffffff", "outline-variant": "#c6c6cd", "on-secondary-fixed-variant": "#3a485c",
                        "on-primary-fixed": "#131b2e", "on-secondary-container": "#57657b", "on-tertiary-fixed-variant": "#444749",
                        "on-primary-fixed-variant": "#3f465c", "inverse-on-surface": "#f3f0f2", "background": "#fcf8fa",
                        "surface": "#fcf8fa", "surface-container-low": "#f6f3f5", "primary-container": "#131b2e",
                        "primary-fixed": "#dae2fd", "surface-container": "#f0edef", "on-surface-variant": "#45464d",
                        "surface-tint": "#565e74", "tertiary-container": "#191c1e", "on-secondary-fixed": "#0d1c2f",
                        "error": "#ba1a1a", "secondary-container": "#d5e3fd", "surface-container-high": "#eae7e9",
                        "on-primary": "#ffffff", "outline": "#76777d", "surface-dim": "#dcd9db", "surface-bright": "#fcf8fa",
                        "on-error-container": "#93000a"
                    },
                    "borderRadius": { "DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px" },
                    "spacing": { "max-width": "1440px", "container-padding": "24px", "gutter": "16px", "stack-md": "16px", "unit": "4px", "stack-lg": "32px", "stack-sm": "8px" },
                    "fontFamily": {
                        "body-sm": ["Inter"], "title-lg": ["Inter"], "headline-md": ["Inter"], "body-md": ["Inter"],
                        "title-md": ["Inter"], "data-tabular": ["Inter"], "headline-sm": ["Inter"], "display-lg": ["Inter"],
                        "label-md": ["Inter"], "body-lg": ["Inter"]
                    },
                    "fontSize": {
                        "body-sm": ["13px", { "lineHeight": "18px", "fontWeight": "400" }],
                        "title-lg": ["18px", { "lineHeight": "24px", "fontWeight": "600" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
                        "body-md": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "title-md": ["16px", { "lineHeight": "24px", "fontWeight": "600" }],
                        "data-tabular": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "display-lg": ["32px", { "lineHeight": "40px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "body-lg": ["16px", { "lineHeight": "24px", "fontWeight": "400" }]
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
        .glass-panel { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); border: 1px solid #E2E8F0; }
        .bento-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }
        .sidebar-nav-item {
            display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 8px;
            color: var(--on-surface-variant); transition: all 0.2s; cursor: pointer;
        }
        .sidebar-nav-item:hover { background-color: var(--surface-container-high); }
        .sidebar-nav-item.active {
            background-color: var(--secondary-container);
            color: var(--on-secondary-container);
            font-weight: 600;
        }
        
        /* Modal sliding styles */
        .slide-over {
            position: fixed; top: 0; right: -100%; width: 100%; max-width: 900px; height: 100vh;
            background: #f8fafc; z-index: 100; transition: right 0.3s ease-in-out;
            box-shadow: -4px 0 24px rgba(0,0,0,0.1); overflow-y: auto;
        }
        .slide-over.active { right: 0; }
        .slide-over-backdrop {
            position: fixed; top: 0; left: 0; width: 100%; height: 100vh;
            background: rgba(0,0,0,0.4); z-index: 90; opacity: 0; pointer-events: none;
            transition: opacity 0.3s ease-in-out;
        }
        .slide-over-backdrop.active { opacity: 1; pointer-events: auto; }
    </style>
</head>
<body class="bg-background text-on-background antialiased flex selection:bg-primary-fixed selection:text-on-primary-fixed">

<!-- SideNavBar -->
<nav class="bg-surface border-r border-outline-variant h-screen w-72 fixed left-0 top-0 flex flex-col p-4 gap-stack-md z-20">
    <div class="flex items-center gap-3 mb-6 px-2">
        <div class="w-10 h-10 rounded bg-primary-container flex items-center justify-center text-on-primary">
            <span class="material-symbols-outlined">shield</span>
        </div>
        <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary">Grahak Kavach</h1>
            <p class="font-body-sm text-body-sm text-on-surface-variant">Officer Portal</p>
        </div>
    </div>
    <div class="flex flex-col gap-2">
        <a class="sidebar-nav-item active" id="nav-overview" onclick="switchTab('overview')">
            <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
            <span class="font-body-md text-body-md">Overview</span>
        </a>
        <a class="sidebar-nav-item" id="nav-complaints" onclick="switchTab('complaints')">
            <span class="material-symbols-outlined">pending_actions</span>
            <span class="font-body-md text-body-md">Pending Cases</span>
        </a>
        <a class="sidebar-nav-item" id="nav-heatmap" onclick="switchTab('heatmap')">
            <span class="material-symbols-outlined">map</span>
            <span class="font-body-md text-body-md">Live Heatmap</span>
        </a>
        <a class="sidebar-nav-item" id="nav-log" onclick="switchTab('log')">
            <span class="material-symbols-outlined">add_circle</span>
            <span class="font-body-md text-body-md">Log Inspection</span>
        </a>
        <a class="sidebar-nav-item" id="nav-my" onclick="switchTab('my')">
            <span class="material-symbols-outlined">assignment</span>
            <span class="font-body-md text-body-md">My Inspections</span>
        </a>
        <a class="sidebar-nav-item" id="nav-legal" onclick="switchTab('legal')">
            <span class="material-symbols-outlined">gavel</span>
            <span class="font-body-md text-body-md">Legal Docs</span>
        </a>
    </div>
    <div class="mt-auto pt-4 border-t border-outline-variant">
        <div class="flex justify-between items-center px-2">
            <div class="flex items-center gap-3">
                <img class="w-8 h-8 rounded-full object-cover" src="assets/logo.svg" style="filter: invert(0.8) sepia(1) hue-rotate(180deg);" />
                <div class="flex flex-col">
                    <span class="font-title-md text-title-md text-primary">Officer</span>
                    <span class="font-body-sm text-body-sm text-on-surface-variant">Logged in</span>
                </div>
            </div>
            <button onclick="logout()" class="text-error hover:bg-error-container p-2 rounded-full transition-colors" title="Logout">
                <span class="material-symbols-outlined">logout</span>
            </button>
        </div>
    </div>
</nav>

<!-- Main Content Area -->
<div class="flex-1 ml-72 flex flex-col min-h-screen">
    <!-- TopAppBar -->
    <header class="bg-surface h-16 sticky top-0 border-b border-outline-variant flex justify-between items-center px-6 z-10 w-full">
        <div class="flex items-center gap-4 bg-surface-container-low rounded-lg px-3 py-2 w-96 border border-outline-variant focus-within:border-primary transition-colors">
            <span class="material-symbols-outlined text-on-surface-variant">search</span>
            <input class="bg-transparent border-none outline-none w-full font-body-md text-body-md text-on-surface placeholder:text-on-surface-variant" placeholder="Search cases, IDs..." type="text"/>
        </div>
        <div class="flex items-center gap-4">
            <div class="lang-container mr-4">
              <select class="lang-switcher bg-surface-container-low border border-outline-variant rounded p-1 font-body-sm text-on-surface">
                <option value="en">EN</option>
                <option value="mr">MR</option>
                <option value="hi">HI</option>
              </select>
            </div>
            <button class="text-on-surface-variant hover:text-primary transition-colors relative">
                <span class="material-symbols-outlined">notifications</span>
                <span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full"></span>
            </button>
        </div>
    </header>

    <main class="p-container-padding flex-1">
    
        <!-- SECTION: OVERVIEW -->
        <div id="section-overview" style="display: block;">
            <div class="mb-stack-lg">
                <h2 class="font-display-lg text-display-lg text-primary">Dashboard Overview</h2>
                <p class="font-body-lg text-body-lg text-on-surface-variant mt-1">Real-time metrics and priority items for your jurisdiction.</p>
            </div>
            
            <div class="bento-grid mb-stack-lg">
                <div class="col-span-12 md:col-span-4 glass-panel rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-[#D97706]">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-10 h-10 rounded-full bg-[#FEF3C7] flex items-center justify-center text-[#D97706]">
                            <span class="material-symbols-outlined">hourglass_empty</span>
                        </div>
                        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Open Cases</span>
                    </div>
                    <div>
                        <div class="font-display-lg text-display-lg text-primary" id="overview-open-count">-</div>
                    </div>
                </div>
                
                <div class="col-span-12 md:col-span-4 glass-panel rounded-xl p-4 flex flex-col justify-between border-l-4 border-l-error">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-10 h-10 rounded-full bg-error-container flex items-center justify-center text-error">
                            <span class="material-symbols-outlined">priority_high</span>
                        </div>
                        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">High Priority</span>
                    </div>
                    <div>
                        <div class="font-display-lg text-display-lg text-primary" id="overview-high-count">-</div>
                    </div>
                </div>

                <div class="col-span-12 md:col-span-4 glass-panel rounded-xl p-4 flex flex-col justify-between">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-10 h-10 rounded-full bg-[#D1FAE5] flex items-center justify-center text-[#059669]">
                            <span class="material-symbols-outlined">task_alt</span>
                        </div>
                        <span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Resolution Rate</span>
                    </div>
                    <div>
                        <div class="font-display-lg text-display-lg text-primary">85%</div>
                        <div class="w-full bg-surface-container-high rounded-full h-1.5 mt-2">
                            <div class="bg-[#059669] h-1.5 rounded-full" style="width: 85%"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="glass-panel rounded-xl flex flex-col p-6 mt-4">
                <h3 class="font-title-lg text-title-lg text-primary mb-6">Complaint Volume Over Time</h3>
                <div class="flex-grow flex items-center justify-center min-h-[300px] border-b border-l border-outline-variant relative">
                    <div class="absolute bottom-0 left-0 w-full h-full flex items-end px-2 space-x-2 opacity-60">
                        <div class="flex-1 bg-secondary-fixed h-1/4 rounded-t"></div>
                        <div class="flex-1 bg-secondary-fixed h-1/3 rounded-t"></div>
                        <div class="flex-1 bg-secondary-fixed h-1/2 rounded-t"></div>
                        <div class="flex-1 bg-secondary-fixed h-2/5 rounded-t"></div>
                        <div class="flex-1 bg-secondary-fixed h-3/5 rounded-t"></div>
                        <div class="flex-1 bg-primary h-3/4 rounded-t"></div>
                        <div class="flex-1 bg-secondary-fixed h-2/3 rounded-t"></div>
                    </div>
                    <span class="text-on-surface-variant font-body-sm italic z-10 bg-surface-container-lowest px-2 shadow">Weekly Trend Data</span>
                </div>
            </div>
        </div>

        <!-- SECTION: COMPLAINTS -->
        <div id="section-complaints" style="display: none;">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-stack-md gap-4">
                <div>
                    <h2 class="font-headline-md text-headline-md text-on-surface">Pending Cases</h2>
                    <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Manage and assign open grievances.</p>
                </div>
                <div class="flex gap-3">
                    <button class="h-10 px-4 rounded border border-outline-variant bg-surface text-on-surface hover:bg-surface-container-high transition-colors font-title-md text-body-md flex items-center gap-2">
                        <span class="material-symbols-outlined text-[18px]">download</span> Export
                    </button>
                </div>
            </div>

            <!-- Filters Bar -->
            <div class="bg-surface rounded border border-outline-variant p-4 mb-stack-md flex flex-wrap gap-4 items-center shadow-sm">
                <span class="font-title-sm text-body-md text-on-surface-variant flex items-center gap-2 border-r border-outline-variant pr-4">
                    <span class="material-symbols-outlined text-[18px]">filter_list</span> Filters
                </span>
                <div class="flex gap-3">
                    <select class="h-9 px-3 py-1 bg-surface-container-low border border-outline-variant rounded focus:outline-none focus:ring-2 focus:ring-primary font-body-sm text-on-surface">
                        <option value="">All Priorities</option>
                    </select>
                    <select class="h-9 px-3 py-1 bg-surface-container-low border border-outline-variant rounded focus:outline-none focus:ring-2 focus:ring-primary font-body-sm text-on-surface">
                        <option value="">All Categories</option>
                    </select>
                </div>
            </div>

            <!-- Data Table -->
            <div class="bg-surface rounded border border-outline-variant shadow-sm overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-surface-container-low border-b border-outline-variant text-on-surface-variant font-label-md text-label-md uppercase h-12">
                                <th class="px-4 py-3 font-semibold">Case ID</th>
                                <th class="px-4 py-3 font-semibold">Consumer</th>
                                <th class="px-4 py-3 font-semibold">Company / Shop</th>
                                <th class="px-4 py-3 font-semibold">Category</th>
                                <th class="px-4 py-3 font-semibold">Date Filed</th>
                                <th class="px-4 py-3 font-semibold">Priority</th>
                                <th class="px-4 py-3 font-semibold">Status</th>
                                <th class="px-4 py-3 font-semibold text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="complaints-queue" class="font-data-tabular text-data-tabular text-on-surface divide-y divide-outline-variant/50">
                            <!-- Populated via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- SECTION: HEATMAP -->
        <div id="section-heatmap" style="display: none;">
            <div class="mb-stack-md">
                <h2 class="font-headline-md text-headline-md text-on-surface">Live Violation Heatmap</h2>
                <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Visualizing complaints across your jurisdiction based on citizen Geo-Tags.</p>
            </div>
            <div class="bg-surface p-4 rounded-xl border border-outline-variant shadow-sm h-[600px] flex flex-col">
                <div id="map" style="flex:1; border-radius: 8px; z-index: 1;"></div>
            </div>
        </div>

        <!-- SECTION: LOG INSPECTION -->
        <div id="section-log" style="display: none;">
            <div class="mb-stack-md">
                <h2 class="font-headline-md text-headline-md text-on-surface">Log a New Inspection</h2>
                <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Record findings from your field visits.</p>
            </div>
            <div class="max-w-2xl bg-surface p-8 rounded-xl border border-outline-variant shadow-sm">
                <form id="log-inspection-form" onsubmit="submitInspection(event)" class="space-y-6">
                    <div>
                        <label class="block font-label-md text-on-surface-variant uppercase tracking-wider mb-2">Shop ID</label>
                        <input type="number" id="insp-shop-id" class="w-full bg-surface-container-lowest border border-outline-variant rounded p-3 font-body-md focus:outline-none focus:ring-2 focus:ring-primary" required>
                    </div>
                    <div>
                        <label class="block font-label-md text-on-surface-variant uppercase tracking-wider mb-2">Product Scanned</label>
                        <input type="text" id="insp-product" class="w-full bg-surface-container-lowest border border-outline-variant rounded p-3 font-body-md focus:outline-none focus:ring-2 focus:ring-primary" required>
                    </div>
                    <div>
                        <label class="block font-label-md text-on-surface-variant uppercase tracking-wider mb-2">Is Compliant?</label>
                        <select id="insp-compliant" class="w-full bg-surface-container-lowest border border-outline-variant rounded p-3 font-body-md focus:outline-none focus:ring-2 focus:ring-primary" required>
                            <option value="true">Yes, Compliant</option>
                            <option value="false">No, Violation Found</option>
                        </select>
                    </div>
                    <div>
                        <label class="block font-label-md text-on-surface-variant uppercase tracking-wider mb-2">Violation Details</label>
                        <textarea id="insp-details" class="w-full bg-surface-container-lowest border border-outline-variant rounded p-3 font-body-md focus:outline-none focus:ring-2 focus:ring-primary min-h-[100px]"></textarea>
                    </div>
                    <button type="submit" class="w-full py-3 bg-primary text-on-primary font-title-md rounded hover:bg-on-surface transition-colors shadow-sm">Submit Inspection</button>
                </form>
            </div>
        </div>

        <!-- SECTION: MY INSPECTIONS -->
        <div id="section-my" style="display: none;">
            <div class="mb-stack-md">
                <h2 class="font-headline-md text-headline-md text-on-surface">My Inspections</h2>
                <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">History of your logged field checks.</p>
            </div>
            <div class="bg-surface rounded border border-outline-variant shadow-sm overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-surface-container-low border-b border-outline-variant text-on-surface-variant font-label-md text-label-md uppercase h-12">
                                <th class="px-4 py-3 font-semibold">ID</th>
                                <th class="px-4 py-3 font-semibold">Shop ID</th>
                                <th class="px-4 py-3 font-semibold">Product Scanned</th>
                                <th class="px-4 py-3 font-semibold">Compliant</th>
                                <th class="px-4 py-3 font-semibold">Date Logged</th>
                            </tr>
                        </thead>
                        <tbody id="my-inspections-list" class="font-data-tabular text-on-surface divide-y divide-outline-variant/50">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- SECTION: LEGAL -->
        <div id="section-legal" style="display: none;">
            <div class="mb-stack-md">
                <h2 class="font-headline-md text-headline-md text-on-surface">Legal Metrology Documents</h2>
                <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Reference acts, and rules for inspections.</p>
            </div>
            <div class="bg-surface rounded border border-outline-variant shadow-sm overflow-hidden">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-surface-container-low border-b border-outline-variant text-on-surface-variant font-label-md text-label-md uppercase h-12">
                            <th class="px-4 py-3 font-semibold">Category</th>
                            <th class="px-4 py-3 font-semibold">Title</th>
                            <th class="px-4 py-3 font-semibold">Action</th>
                        </tr>
                    </thead>
                    <tbody id="legal-docs-list" class="font-data-tabular text-on-surface divide-y divide-outline-variant/50">
                    </tbody>
                </table>
            </div>
        </div>
        
    </main>
</div>

<!-- SLIDE-OVER CASE DETAILS (Replaces Modal) -->
<div class="slide-over-backdrop" id="slide-over-backdrop" onclick="closeSlideOver()"></div>
<div class="slide-over" id="slide-over-panel">
    <div class="h-full flex flex-col">
        <!-- Header -->
        <div class="bg-surface p-6 border-b border-outline-variant sticky top-0 z-10 flex justify-between items-center">
            <div>
                <div class="flex items-center gap-3 mb-2">
                    <span class="font-title-lg text-title-lg text-primary" id="so-tracking-id">Case #---</span>
                    <span class="px-3 py-1 bg-surface-container-high text-on-surface-variant font-label-md rounded-full border border-outline-variant" id="so-violation-badge">Type</span>
                </div>
                <h2 class="font-headline-sm text-headline-sm text-on-surface font-semibold" id="so-shop-name">Shop Name</h2>
            </div>
            <div class="flex gap-3">
                <button onclick="closeSlideOver()" class="p-2 text-on-surface-variant hover:bg-surface-container-high rounded-full transition-colors">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
        </div>
        
        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-6 bg-surface-container-lowest">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Left Col -->
                <div class="flex flex-col gap-6">
                    <!-- Consumer Profile -->
                    <div class="bg-surface p-6 rounded-xl border border-outline-variant">
                        <h3 class="font-title-lg text-on-surface mb-4 flex items-center gap-2 border-b border-outline-variant pb-2">
                            <span class="material-symbols-outlined text-secondary">person</span> Consumer Profile
                        </h3>
                        <div class="grid grid-cols-1 gap-4">
                            <div>
                                <p class="font-label-md text-on-surface-variant uppercase tracking-wider mb-1">Full Name</p>
                                <p class="font-body-lg text-on-surface font-medium" id="so-user-name">---</p>
                            </div>
                            <div>
                                <p class="font-label-md text-on-surface-variant uppercase tracking-wider mb-1">Contact</p>
                                <p class="font-body-md text-on-surface" id="so-user-email">---</p>
                            </div>
                            <div id="so-location-container" style="display:none;">
                                <p class="font-label-md text-on-surface-variant uppercase tracking-wider mb-1">Location</p>
                                <a id="so-location-link" href="#" target="_blank" class="font-body-md text-primary flex items-center gap-1 hover:underline">
                                    <span class="material-symbols-outlined text-sm">location_on</span> View on Map
                                </a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Complaint Desc -->
                    <div class="bg-surface p-6 rounded-xl border border-outline-variant">
                        <h3 class="font-title-lg text-on-surface mb-4 flex items-center gap-2 border-b border-outline-variant pb-2">
                            <span class="material-symbols-outlined text-secondary">description</span> Complaint Description
                        </h3>
                        <p class="font-body-md text-on-surface-variant leading-relaxed mb-6 whitespace-pre-wrap" id="so-desc">---</p>
                        
                        <h4 class="font-title-md text-on-surface mb-3">Uploaded Evidence</h4>
                        <div id="so-evidence-container">
                            <img id="so-evidence-img" src="" class="w-full rounded-lg border border-outline-variant cursor-pointer hover:opacity-90 transition-opacity" style="display:none; max-height: 250px; object-fit: contain; background: #f8fafc;" onclick="window.open(this.src, '_blank')">
                            <div id="so-no-evidence" class="text-on-surface-variant p-4 border border-outline-variant border-dashed rounded-lg text-center font-body-sm">
                                No evidence uploaded.
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Right Col -->
                <div class="flex flex-col gap-6">
                    <!-- Action Panel -->
                    <div class="bg-surface p-6 rounded-xl border border-outline-variant shadow-sm">
                        <h3 class="font-title-lg text-on-surface mb-4 flex items-center gap-2 border-b border-outline-variant pb-2">
                            <span class="material-symbols-outlined text-secondary">task_alt</span> Action Panel
                        </h3>
                        <div class="mb-4">
                            <label class="block font-label-md text-on-surface-variant uppercase tracking-wider mb-2">Update Status</label>
                            <select id="so-status" class="w-full rounded border border-outline-variant bg-surface-container-lowest p-3 font-body-md focus:ring-2 focus:ring-primary focus:border-primary">
                                <option value="Pending">Pending</option>
                                <option value="Verified">Verified</option>
                                <option value="In Progress">In Progress</option>
                                <option value="Resolved">Resolved</option>
                            </select>
                        </div>
                        <button id="save-status-btn" onclick="saveComplaintStatus()" class="w-full py-3 bg-primary text-on-primary font-title-md rounded hover:bg-tertiary-container transition-colors shadow-sm mt-2">
                            Save Changes
                        </button>
                    </div>
                    
                    <!-- Case Timeline -->
                    <div class="bg-surface p-6 rounded-xl border border-outline-variant">
                        <h3 class="font-title-lg text-on-surface mb-4 flex items-center gap-2 border-b border-outline-variant pb-2">
                            <span class="material-symbols-outlined text-secondary">timeline</span> Case Timeline
                        </h3>
                        <div class="relative border-l-2 border-outline-variant ml-4 mt-4 space-y-6 pb-4">
                            <div class="relative pl-6">
                                <div class="absolute w-4 h-4 bg-primary rounded-full -left-[9px] top-1 border-2 border-surface"></div>
                                <p class="font-label-md text-on-surface-variant mb-1" id="so-date-filed">---</p>
                                <p class="font-title-md text-on-surface">Case Filed by Consumer</p>
                                <p class="font-body-sm text-on-surface-variant mt-1" id="so-verification-method">---</p>
                            </div>
                            <div class="relative pl-6">
                                <div class="absolute w-4 h-4 bg-error rounded-full -left-[9px] top-1 border-2 border-surface"></div>
                                <p class="font-title-md text-error font-semibold">Current Status</p>
                                <p class="font-body-sm text-on-surface-variant mt-1" id="so-current-status">---</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script defer src="js/translations.js"></script>
<script defer src="js/i18n.js"></script>
<script defer src="js/api.js"></script>
<script>
    let currentQueue = [];
    let activeTrackingId = null;

    function openSlideOver(trackingId) {
        const comp = currentQueue.find(c => c.tracking_id === trackingId);
        if(!comp) return;
        
        activeTrackingId = trackingId;
        document.getElementById('so-tracking-id').textContent = 'Case #' + comp.tracking_id;
        document.getElementById('so-violation-badge').textContent = comp.violation_type + ' Violation';
        document.getElementById('so-shop-name').textContent = comp.shop_name || 'Unknown Shop';
        
        document.getElementById('so-user-name').textContent = comp.user_name || 'N/A';
        document.getElementById('so-user-email').textContent = comp.user_email || 'N/A';
        
        if (comp.latitude && comp.longitude) {
            document.getElementById('so-location-container').style.display = 'block';
            document.getElementById('so-location-link').href = `https://www.google.com/maps?q=${comp.latitude},${comp.longitude}`;
        } else {
            document.getElementById('so-location-container').style.display = 'none';
        }
        
        document.getElementById('so-desc').textContent = comp.product_details || 'No description provided.';
        document.getElementById('so-status').value = comp.status;
        
        document.getElementById('so-date-filed').textContent = new Date(comp.date_filed).toLocaleString();
        document.getElementById('so-current-status').textContent = comp.status;
        document.getElementById('so-verification-method').textContent = "Verified via " + (comp.verification_method || 'Email');
        
        const img = document.getElementById('so-evidence-img');
        const noImg = document.getElementById('so-no-evidence');
        if (comp.evidence_url) {
            img.src = comp.evidence_url;
            img.style.display = 'block';
            noImg.style.display = 'none';
        } else {
            img.style.display = 'none';
            noImg.style.display = 'block';
        }

        document.getElementById('slide-over-panel').classList.add('active');
        document.getElementById('slide-over-backdrop').classList.add('active');
    }
    
    function closeSlideOver() {
        document.getElementById('slide-over-panel').classList.remove('active');
        document.getElementById('slide-over-backdrop').classList.remove('active');
    }

    async function saveComplaintStatus() {
        if(!activeTrackingId) return;
        const newStatus = document.getElementById('so-status').value;
        const btn = document.getElementById('save-status-btn');
        
        try {
            btn.textContent = 'Saving...';
            await API.updateComplaintStatus(activeTrackingId, newStatus);
            closeSlideOver();
            loadDashboardData(); 
        } catch(e) {
            console.error(e);
            alert('Failed to update status');
        } finally {
            btn.textContent = 'Save Changes';
        }
    }

    async function loadDashboardData() {
        try {
            currentQueue = await API.getComplaintsQueue();
            const tbody = document.getElementById('complaints-queue');
            tbody.innerHTML = '';
            
            let openCount = 0;
            let highPriorityCount = 0;

            if (currentQueue.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="text-center py-8 text-on-surface-variant">No complaints in queue.</td></tr>';
                document.getElementById('overview-open-count').textContent = '0';
                document.getElementById('overview-high-count').textContent = '0';
                return;
            }

            currentQueue.forEach(comp => {
                if (comp.status !== 'Resolved') openCount++;
                
                const isHighPriority = comp.violation_type === 'Food Safety' || comp.violation_type === 'Both';
                if (isHighPriority && comp.status !== 'Resolved') highPriorityCount++;
                
                const priority = isHighPriority ? 'High' : 'Medium';
                const pColorClass = isHighPriority ? 'bg-error-container text-on-error-container' : 'bg-surface-variant text-on-surface-variant';
                const pDotClass = isHighPriority ? 'bg-error' : 'bg-outline';
                
                // Status styling
                let sColorClass = 'bg-surface-container-high border-outline-variant text-on-surface-variant';
                if(comp.status === 'Verified') sColorClass = 'bg-[#DBEAFE] border-[#BFDBFE] text-[#1D4ED8]';
                if(comp.status === 'In Progress') sColorClass = 'bg-secondary-container border-secondary-fixed text-on-secondary-container';
                if(comp.status === 'Resolved') sColorClass = 'bg-[#D1FAE5] border-[#A7F3D0] text-[#047857]';

                const dateStr = new Date(comp.date_filed).toLocaleDateString();

                tbody.innerHTML += `
                    <tr class="h-16 hover:bg-surface-container-lowest transition-colors border-b border-surface-variant group">
                        <td class="px-4 py-3"><a class="text-secondary font-semibold hover:underline cursor-pointer" onclick="openSlideOver('${comp.tracking_id}')">#${comp.tracking_id}</a></td>
                        <td class="px-4 py-3">${comp.user_name || 'Anonymous'}</td>
                        <td class="px-4 py-3 font-medium">${comp.shop ? comp.shop.name : 'Unknown Shop'}</td>
                        <td class="px-4 py-3 text-on-surface-variant">${comp.violation_type}</td>
                        <td class="px-4 py-3 text-on-surface-variant">${dateStr}</td>
                        <td class="px-4 py-3">
                            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full ${pColorClass} font-label-md">
                                <span class="w-1.5 h-1.5 rounded-full ${pDotClass}"></span> ${priority}
                            </span>
                        </td>
                        <td class="px-4 py-3">
                            <span class="inline-flex items-center px-2.5 py-1 rounded-full border font-body-sm text-[11px] font-medium leading-none ${sColorClass}">
                                ${comp.status}
                            </span>
                        </td>
                        <td class="px-4 py-3 text-right">
                            <button onclick="openSlideOver('${comp.tracking_id}')" class="px-3 py-1.5 bg-primary text-on-primary rounded font-label-md hover:bg-primary-container hover:text-on-primary-container transition-colors opacity-0 group-hover:opacity-100">Review</button>
                        </td>
                    </tr>
                `;
            });
            
            document.getElementById('overview-open-count').textContent = openCount;
            document.getElementById('overview-high-count').textContent = highPriorityCount;

        } catch (e) {
            console.error(e);
            document.getElementById('complaints-queue').innerHTML = '<tr><td colspan="8" class="text-center py-8 text-error">Failed to load queue.</td></tr>';
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const token = localStorage.getItem('officer_token');
        if (!token) {
            window.location.href = 'officer-login.html';
            return;
        }
        loadDashboardData();
        initWebSocket();
    });

    function switchTab(tab) {
        document.querySelectorAll('.sidebar-nav-item').forEach(el => el.classList.remove('active'));
        document.getElementById('nav-' + tab).classList.add('active');
        
        ['overview', 'complaints', 'heatmap', 'log', 'my', 'legal'].forEach(t => {
            document.getElementById('section-' + t).style.display = 'none';
        });
        
        document.getElementById('section-' + tab).style.display = 'block';

        if (tab === 'my') loadMyInspections();
        if (tab === 'complaints' || tab === 'overview') loadDashboardData();
        if (tab === 'legal') loadLegalDocs();
        if (tab === 'heatmap') renderHeatmap();
    }

    function logout() {
        localStorage.removeItem('officer_token');
        window.location.href = 'index.html';
    }

    async function submitInspection(e) {
        e.preventDefault();
        const shopId = document.getElementById('insp-shop-id').value;
        const product = document.getElementById('insp-product').value;
        const compliant = document.getElementById('insp-compliant').value === 'true';
        const details = document.getElementById('insp-details').value;
        try {
            await API.logInspection({ shop_id: parseInt(shopId), product_scanned: product, is_compliant: compliant, violation_details: details || null });
            alert('Inspection logged successfully!');
            document.getElementById('log-inspection-form').reset();
            switchTab('my');
        } catch(err) {
            console.error(err);
            alert('Failed to log inspection. Does the Shop ID exist?');
        }
    }

    async function loadMyInspections() {
        const tbody = document.getElementById('my-inspections-list');
        tbody.innerHTML = '<tr><td colspan="5" class="text-center py-8">Loading...</td></tr>';
        try {
            const data = await API.getMyInspections();
            tbody.innerHTML = '';
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center py-8 text-on-surface-variant">No inspections logged yet.</td></tr>';
                return;
            }
            data.forEach(insp => {
                const dateStr = new Date(insp.date_logged).toLocaleDateString();
                const compStr = insp.is_compliant 
                    ? '<span class="text-[#059669] font-medium">Yes</span>' 
                    : '<span class="text-error font-medium">No</span>';
                tbody.innerHTML += `
                    <tr class="h-14 border-b border-outline-variant/50 hover:bg-surface-container-lowest">
                        <td class="px-4 py-3 font-medium">#${insp.id}</td>
                        <td class="px-4 py-3">${insp.shop_id}</td>
                        <td class="px-4 py-3">${insp.product_scanned}</td>
                        <td class="px-4 py-3">${compStr}</td>
                        <td class="px-4 py-3 text-on-surface-variant">${dateStr}</td>
                    </tr>
                `;
            });
        } catch(err) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center py-8 text-error">Failed to load inspections.</td></tr>';
        }
    }

    async function loadLegalDocs() {
        const tbody = document.getElementById('legal-docs-list');
        tbody.innerHTML = '<tr><td colspan="3" class="text-center py-8">Loading...</td></tr>';
        try {
            const data = await API.getLegalMetrologyDocs();
            tbody.innerHTML = '';
            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center py-8">No documents available.</td></tr>';
                return;
            }
            data.sort((a, b) => a.category.localeCompare(b.category));
            data.forEach(doc => {
                tbody.innerHTML += `
                    <tr class="h-14 border-b border-outline-variant/50 hover:bg-surface-container-lowest">
                        <td class="px-4 py-3"><span class="bg-surface-container-high px-2 py-1 rounded text-xs font-medium">${doc.category}</span></td>
                        <td class="px-4 py-3 font-medium">${doc.title}</td>
                        <td class="px-4 py-3"><a href="${doc.url}" target="_blank" class="text-primary hover:underline font-medium">Download</a></td>
                    </tr>
                `;
            });
        } catch(err) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center py-8 text-error">Failed to load documents.</td></tr>';
        }
    }

    let heatmapMap = null;
    function renderHeatmap() {
        if (!heatmapMap) {
            heatmapMap = L.map('map').setView([19.7515, 75.7139], 6);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(heatmapMap);
        }
        if (heatmapMap.markerLayer) heatmapMap.removeLayer(heatmapMap.markerLayer);
        heatmapMap.markerLayer = L.layerGroup().addTo(heatmapMap);
        
        currentQueue.forEach(comp => {
            if (comp.latitude && comp.longitude) {
                const marker = L.marker([comp.latitude, comp.longitude]);
                marker.bindPopup(`<b>#${comp.tracking_id}</b><br>${comp.violation_type} Violation<br>Status: ${comp.status}`);
                heatmapMap.markerLayer.addLayer(marker);
            }
        });
        setTimeout(() => heatmapMap.invalidateSize(), 100);
    }

    function initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = API_BASE_URL.replace(/^https?:\/\//, '');
        const wsUrl = `${protocol}//${host}/ws`;
        const ws = new WebSocket(wsUrl);
        
        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === "NEW_COMPLAINT" || msg.type === "STATUS_UPDATE") {
                    if (document.getElementById('section-complaints').style.display !== 'none' || document.getElementById('section-overview').style.display !== 'none') {
                        loadDashboardData();
                    }
                }
            } catch(e) {}
        };
        ws.onclose = () => setTimeout(initWebSocket, 5000);
    }
</script>
</body>
</html>
"""

    with open('frontend/officer-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_officer_dashboard()
