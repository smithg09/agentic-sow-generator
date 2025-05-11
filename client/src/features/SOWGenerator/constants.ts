export const API_BASE_URL = 'http://127.0.0.1:8080'

export const API_ENDPOINTS = {
    GENERATE_SOW: `${API_BASE_URL}/generate-sow`,
    GENERATED_SOW_PDF: `${API_BASE_URL}/static/Generated_SOW_final.docx`,
    LIKE_SOW: `${API_BASE_URL}/like-sow`,
    CHAT: `${API_BASE_URL}/chat`,
}

export const DEFAULT_VALUES = {
    projectObjectives: `The Client operates a complex on-premise environment, primarily leveraging Microsoft SQL Server for multiple transactional systems, both homegrown and commercial. These systems encompass transportation management, order management, finished vehicle tracking, inspections, and claims processing. While these systems generate substantial data volumes, they offer limited analytical and reporting capabilities. Currently, different departments rely on a centralized BI function for ad-hoc reporting, which creates bottlenecks in data access and strains the transactional databases`,
    projectScope: `The Discovery and Assessment phase will be considered complete upon delivery and acceptance of:
5.1.	All documented deliverables outlined in Section 3
5.2.	Final presentation of findings and recommendations
5.3.	Proposed implementation roadmap
`,
    servicesDescription: `[PROVIDER_NAME] will provide the following Services: 
2.1.	Stakeholder Engagement and Current State Analysis A thorough review of existing systems and processes through structured interviews and documentation review.
2.2.	Technical Evaluation Detailed assessment of current architecture, system capabilities, and integration points.
2.3.	Gap Analysis and Recommendations Comprehensive analysis of current state versus industry best practices, leading to actionable recommendations.
2.4.	Implementation Planning Development of a strategic roadmap for modernizing the data platform environment.
`,
    specificFeatures: `The Discovery and Assessment phase will be considered complete upon delivery and acceptance of:
5.1.	All documented deliverables outlined in Section 3
5.2.	Final presentation of findings and recommendations
5.3.	Proposed implementation roadmap
`,
    platformsTechnologies: "",
    integrations: "",
    designSpecifications: "",
    outOfScope: `As a condition for recovery of any liability, the parties must assert any claim under this SOW within three (3) months after discovery or sixty (60) days after the termination or expiration of this SOW, whichever is earlier. In no event will either party to this Agreement be liable for incidental, consequential, punitive, indirect or special damages, including, without limitation, interruption or loss of business, profit or goodwill.  In no event shall [PROVIDER_NAME]'s liability to Client exceed the fees received from Client under this SOW during the six (6) month period preceding the claim to which the liability relates, whether arising from an alleged breach of the Agreement or this SOW, an alleged tort, or any other cause of action.`,
    deliverables: `.  [PROVIDER_NAME] will provide the following Deliverables: 
3.1.	Current State Analysis report of existing systems, data flows, and identified opportunities for improvement.
3.2.	Technical Assessment report with detailed evaluation of current architecture, including integration analysis and technology stack assessment.
3.3.	Final Recommendations report of complete modernization strategy including target architecture, implementation roadmap, and strategy
`,
    timeline: `. The Services and Deliverables shall be delivered in accordance with the following schedule:
4.1.	Discovery (Weeks 1-3)
•	Stakeholder interviews
•	System documentation review
•	Initial findings compilation
4.2.	Technical Analysis (Weeks 4-5)
•	Architecture evaluation
•	Integration assessment
•	Technology stack review
4.3.	Feasibility Evaluation (Weeks 6-7)
•	Gap analysis
•	Recommendations
4.4.	Final Recommendations (Weeks 8-10)
•	Roadmap development
•	Final deliverable preparation
`,
}