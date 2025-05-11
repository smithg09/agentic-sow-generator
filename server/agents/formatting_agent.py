import os
import docx
from docx.shared import Pt

class FormattingAgent:
    def __init__(self):
        pass

    def generate_sow_document(self, sow_data, output_filename="Generated_SOW_final.docx"):
        """Generate a DOCX document from SOW data"""
        markdown = ''
        newLineChar = '\n\n'
        doc = docx.Document()
        doc.add_heading(sow_data["Project Name"], level=1)
        markdown += f'## {sow_data["Project Name"]}\n\n'
        
        intro = (f"This Statement of Work (“SOW”) is entered into as of {sow_data['SOW Effective Date']} by and between "
             f"{sow_data['Company Information']} (“{sow_data['Company Name']}”) and {sow_data['Client']} (“{sow_data['Client Name'] or 'Client'}”) under the provisions of "
             f"that certain Master Services Agreement, dated as of {sow_data['Agreement Date']}, by and between {sow_data['Company Name']} and {sow_data['Client Name'] or 'Client'} (the “Agreement”).")
        doc.add_paragraph(intro)
        markdown += f"{intro}{newLineChar}"
        
        section_order = [
            "Services Description", "Deliverables", "Milestones", "Acceptance",
            "Personnel and Locations", "Representatives", "Client Representatives",
            "Contractor Resources", "Terms & Conditions", "Fees", "Expenses", "Taxes", "Conversion",
            "Limitation of Liability", "Service Level Agreement", "Assumptions", "Change Process"
        ]
        for section in section_order:
            doc.add_heading(section, level=1)
            markdown += f"## {section}{newLineChar}"
            try: 
                doc.add_paragraph(sow_data[section])
                markdown += f"{sow_data[section]}{newLineChar}"
            except Exception as e:
                doc.add_paragraph('')
                markdown += newLineChar 
        
        # Additional optional sections
        if "Current State Analysis" in sow_data:
            doc.add_heading("Current State Analysis", level=1)
            markdown += f"## Current State Analysis{newLineChar}"
            doc.add_paragraph(sow_data["Current State Analysis"])
            markdown += f"{sow_data['Current State Analysis']}{newLineChar}"

        if "Gap Analysis" in sow_data:
            doc.add_heading("Gap Analysis", level=1)
            markdown += f"## Gap Analysis{newLineChar}"
            doc.add_paragraph(sow_data["Gap Analysis"])
            markdown += f"{sow_data['Gap Analysis']}{newLineChar}"

        # Signature section
        doc.add_heading("IN WITNESS WHEREOF", level=1)
        markdown += f"IN WITNESS WHEREOF{newLineChar}"
        doc.add_paragraph("Authorized signatures effective as of the effective date of this SOW.")
        markdown += f"Authorized signatures effective as of the effective date of this SOW.{newLineChar}"
        doc.add_paragraph(f"{sow_data['Client Name'] or 'Client'}  Signature: ________________")
        markdown += f"{sow_data['Client Name'] or 'Client'} Signature: ________________{newLineChar}"
        doc.add_paragraph(f"{sow_data['Company Name'] or ''} Signature: ________________")
        markdown += f"{sow_data['Company Name'] or ''} Signature: ________________{newLineChar}"

        # Save document
        static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        output_path = os.path.join(static_folder, output_filename)
        doc.save(output_path)

        print(f"✅ SOW document generated: {output_filename}")
        return {"fileName": output_filename, "formatted_sow_md": markdown}
        
    def process_sow(self, state):
        """Process SOW for formatting"""
        try:
            output_file = self.generate_sow_document(state['validated_sow'])
            state['doc_file_path'] = output_file['fileName']
            state['formatted_sow'] = output_file['formatted_sow_md']
            return state
        except Exception as e:
            state['error'] = f"Document formatting failed: {str(e)}"
            return state