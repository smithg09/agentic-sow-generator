import spacy
from transformers import pipeline
import json

class ComplianceAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.clause_checker = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            framework="pt",
            device=-1
        )
       
        self.required_fields = [
            "Project Title", "Scope of Work", "Deliverables",
            "Timeline", "Payment Terms", "Confidentiality",
            "Termination", "Limitation of Liability"
        ]

    def validate_structure(self, sow_data):
        """Check for missing fields and basic validation"""
        missing = []
        issues = []
        
        for field in self.required_fields:
            value = sow_data.get(field)
            if not value:
                print(f"MISSING {field}:")
                print(sow_data)
                missing.append(field)
                continue
                
            if isinstance(value, list) and not value:
                issues.append(f"{field.replace('_', ' ').title()} list is empty")
            elif isinstance(value, str) and not value.strip():
                issues.append(f"{field.replace('_', ' ').title()} is empty")
        
        return missing, issues

    def analyze_clauses(self, text):
        """AI-powered clause analysis"""
        clauses = ["confidentiality", "termination", "liability"]
        results = self.clause_checker(text, clauses, multi_label=True)
        
        issues = []
        for label, score in zip(results['labels'], results['scores']):
            if score < 0.6:
                issues.append(f"{label.title()} clause needs strengthening ({score:.1%} confidence)")
        return issues

    def check_language(self, text):
        """Language quality checks"""
        doc = self.nlp(text)
        issues = []
        
        # Passive voice detection
        for sent in doc.sents:
            if any(token.dep_ == "nsubjpass" for token in sent):
                issues.append(f"Passive voice: '{sent.text}'")
        
        # Vague terms check
        vague_terms = ["appropriate", "reasonable", "etc."]
        for term in vague_terms:
            if term in text.lower():
                issues.append(f"Vague term used: '{term}'")
        
        return issues

    def generate_report(self, sow_data):
        """Full compliance analysis"""
        report = {
            "missing_fields": [],
            "structural_issues": [],
            "content_issues": [],
            "language_issues": [],
            "compliance_score": 100,
            "risk_level": "low",
            "recommendations": []
        }
        
        # Structural validation
        report["missing_fields"], report["structural_issues"] = self.validate_structure(sow_data)
        
        # Content analysis
        if "sow_text" in sow_data:
            report["content_issues"].extend(self.analyze_clauses(sow_data["sow_text"]))
            report["language_issues"].extend(self.check_language(sow_data["sow_text"]))
        
        # Calculate score
        penalties = (
            len(report["missing_fields"]) * 5 +
            len(report["structural_issues"]) * 3 +
            len(report["content_issues"]) * 2 +
            len(report["language_issues"]) * 1
        )
        report["compliance_score"] = max(0, 100 - penalties)
        
        # Determine risk level
        if report["compliance_score"] >= 85:
            report["risk_level"] = "low"
        elif report["compliance_score"] >= 60:
            report["risk_level"] = "medium"
        else:
            report["risk_level"] = "high"
            
        # Generate recommendations
        if report["missing_fields"]:
            report["recommendations"].append(f"Add missing fields: {', '.join(report['missing_fields'])}")
        if any("confidentiality" in issue.lower() for issue in report["content_issues"]):
            report["recommendations"].append("Include explicit NDA language in confidentiality clause")
        if report["language_issues"]:
            report["recommendations"].append("Revise vague terms and passive voice constructions")
        
        return report

    def process_sow(self, state):
        """Process SOW content for compliance"""
        try:
            # Attempt to parse the SOW as JSON
            try:
                sow_data = json.loads(state['sow'])
            except Exception:
                # If parsing fails, treat the entire text as the content to check
                sow_data = {"sow_text": state['sow']}
            
            # Generate the compliance report
            report = self.generate_report(sow_data)
            state['compliance_results'] = report
            
            # If any compliance issues are detected, build a brief error message
            if (report["compliance_score"] < 80 or
                report["missing_fields"] or
                report["structural_issues"] or
                report["content_issues"] or
                report["language_issues"]):
                error_message = "Compliance issues detected: "
                if report["missing_fields"]:
                    error_message += f"Missing fields: {', '.join(report['missing_fields'])}. "
                if report["structural_issues"]:
                    error_message += f"Structural issues: {', '.join(report['structural_issues'])}. "
                if report["content_issues"]:
                    error_message += f"Content issues: {', '.join(report['content_issues'])}. "
                if report["language_issues"]:
                    error_message += f"Language issues: {', '.join(report['language_issues'])}. "
                error_message += f"Risk Level: {report['risk_level']}"
                state['error'] = error_message
            
            return state
        except Exception as e:
            state['error'] = f"Compliance checking failed: {str(e)}"
            return state