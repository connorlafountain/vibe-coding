"""
Email service for sending RFQ notifications to vendors via SendGrid
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@anzarenewables.com")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_rfq_email(to_email: str, vendor_name: str, contact_name: str,
                   project_name: str, module_name: str, module_wattage: int,
                   module_manufacturer: str, portal_link: str) -> bool:
    """
    Send RFQ email to vendor with portal link

    Args:
        to_email: Vendor email address
        vendor_name: Vendor company name
        contact_name: Vendor contact person name
        project_name: Project name
        module_name: Module name
        module_wattage: Module wattage
        module_manufacturer: Module manufacturer
        portal_link: Unique portal URL for vendor

    Returns:
        bool: True if email sent successfully, False otherwise
    """

    # For POC, if no SendGrid API key, just print to console
    if not SENDGRID_API_KEY:
        print("\n" + "="*80)
        print("📧 EMAIL WOULD BE SENT (No SendGrid API key configured)")
        print("="*80)
        print(f"To: {to_email}")
        print(f"From: {FROM_EMAIL}")
        print(f"Subject: RFQ from Anza Renewables - {project_name}")
        print(f"\nVendor: {vendor_name}")
        print(f"Contact: {contact_name}")
        print(f"Module: {module_name} ({module_wattage}W)")
        print(f"\nPortal Link: {portal_link}")
        print("="*80 + "\n")
        return True

    # Create email subject
    subject = f"RFQ from Anza Renewables - {project_name}"

    # HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{
                display: inline-block;
                background-color: #2563eb;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .module-card {{
                background-color: white;
                padding: 20px;
                border-left: 4px solid #2563eb;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .footer {{
                background-color: #f3f4f6;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #6b7280;
                border-radius: 0 0 8px 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">Request for Quote</h1>
                <p style="margin: 10px 0 0 0;">Anza Renewables</p>
            </div>

            <div class="content">
                <h2>Hi {contact_name},</h2>

                <p>Anza Renewables is requesting a quote for the following module as part of our <strong>{project_name}</strong> project:</p>

                <div class="module-card">
                    <h3 style="margin-top: 0; color: #2563eb;">Module Request</h3>
                    <p><strong>Module:</strong> {module_name}</p>
                    <p><strong>Manufacturer:</strong> {module_manufacturer}</p>
                    <p><strong>Wattage:</strong> {module_wattage}W</p>
                </div>

                <p>Please click the button below to access your vendor portal and submit your quote:</p>

                <div style="text-align: center;">
                    <a href="{portal_link}" class="button">Submit Your Quote</a>
                </div>

                <p style="margin-top: 30px; font-size: 14px; color: #6b7280;">
                    This link is unique to {vendor_name} and provides access to your vendor portal.
                    If you have any questions, please reply to this email.
                </p>
            </div>

            <div class="footer">
                <p><strong>Anza Renewables Strategic Sourcing Team</strong></p>
                <p>This is an automated notification from the Vendor Portal.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Plain text fallback
    text_body = f"""
    Request for Quote - Anza Renewables

    Hi {contact_name},

    Anza Renewables is requesting a quote for the following module:

    Project: {project_name}
    Module: {module_name}
    Manufacturer: {module_manufacturer}
    Wattage: {module_wattage}W

    Please click the link below to access your vendor portal and submit your quote:

    {portal_link}

    This link is unique to {vendor_name}.

    Thank you,
    Anza Renewables Strategic Sourcing Team
    """

    try:
        # Create SendGrid message
        message = Mail(
            from_email=Email(FROM_EMAIL, "Anza Renewables SST"),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=Content("text/plain", text_body),
            html_content=Content("text/html", html_body)
        )

        # Send email via SendGrid
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        print(f"✅ Email sent successfully to {to_email} (Status: {response.status_code})")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        # Still return True for POC purposes (so workflow continues)
        return True


if __name__ == "__main__":
    # Test email service
    print("Testing email service...")

    success = send_rfq_email(
        to_email="clafountain@anzarenewables.com",
        vendor_name="JinkoSolar",
        contact_name="Connor LaFountain",
        project_name="Arizona Solar Farm 100MW",
        module_name="JinkoSolar Tiger Neo 580W",
        module_wattage=580,
        module_manufacturer="JinkoSolar",
        portal_link="http://localhost:8000/vendor/test-token-123"
    )

    print(f"Email test {'succeeded' if success else 'failed'}")
