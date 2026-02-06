"""
Email service for sending RFQ notifications to vendors
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_rfq_email(to_email: str, vendor_name: str, contact_name: str,
                   project_name: str, modules: list, portal_link: str) -> bool:
    """
    Send RFQ email to vendor with portal link

    Args:
        to_email: Vendor email address
        vendor_name: Vendor company name
        contact_name: Vendor contact person name
        project_name: Project name
        modules: List of Module objects
        portal_link: Unique portal URL for vendor

    Returns:
        bool: True if email sent successfully, False otherwise
    """

    # For POC, if no Gmail credentials, just print to console
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("\n" + "="*60)
        print("📧 EMAIL WOULD BE SENT (No Gmail credentials configured)")
        print("="*60)
        print(f"To: {to_email}")
        print(f"Subject: RFQ from Anza Renewables - {project_name}")
        print(f"\nPortal Link: {portal_link}")
        print("="*60 + "\n")
        return True

    # Create email content
    subject = f"RFQ from Anza Renewables - {project_name}"

    # Build module list
    module_list = "\n".join([
        f"  • {m.name} ({m.wattage}W, {m.manufacturer})"
        for m in modules
    ])

    # HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9fafb; padding: 30px; }}
            .button {{
                display: inline-block;
                background-color: #2563eb;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{ background-color: #f3f4f6; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; }}
            .module-list {{ background-color: white; padding: 15px; border-left: 4px solid #2563eb; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Request for Quote</h1>
                <p>Anza Renewables</p>
            </div>

            <div class="content">
                <h2>Hi {contact_name},</h2>

                <p>Anza Renewables is requesting a quote for the following project:</p>

                <p><strong>Project:</strong> {project_name}</p>

                <div class="module-list">
                    <h3>Modules Requested:</h3>
                    <pre>{module_list}</pre>
                </div>

                <p>Please click the button below to review full project details and submit your quote through our vendor portal:</p>

                <div style="text-align: center;">
                    <a href="{portal_link}" class="button">Submit Your Quote</a>
                </div>

                <p style="margin-top: 30px; font-size: 14px; color: #6b7280;">
                    This link is unique to {vendor_name} and expires in 7 days.
                    If you have any questions, please reply to this email.
                </p>
            </div>

            <div class="footer">
                <p>Anza Renewables Strategic Sourcing Team</p>
                <p>This is an automated email from the Vendor Portal POC.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Plain text fallback
    text_body = f"""
    Request for Quote - Anza Renewables

    Hi {contact_name},

    Anza Renewables is requesting a quote for the following project:

    Project: {project_name}

    Modules Requested:
    {module_list}

    Please click the link below to review full project details and submit your quote:

    {portal_link}

    This link is unique to {vendor_name} and expires in 7 days.

    Thank you,
    Anza Renewables Strategic Sourcing Team
    """

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = to_email

        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


if __name__ == "__main__":
    # Test email service
    print("Testing email service...")

    # Mock module data
    class MockModule:
        def __init__(self, name, wattage, manufacturer):
            self.name = name
            self.wattage = wattage
            self.manufacturer = manufacturer

    test_modules = [
        MockModule("JinkoSolar Tiger Neo 580W", 580, "JinkoSolar"),
        MockModule("Trina Solar Vertex 600W", 600, "Trina Solar"),
    ]

    success = send_rfq_email(
        to_email="test@example.com",
        vendor_name="Test Vendor",
        contact_name="John Doe",
        project_name="Test Solar Project",
        modules=test_modules,
        portal_link="http://localhost:8000/vendor/test-token-123"
    )

    print(f"Email test {'succeeded' if success else 'failed'}")
