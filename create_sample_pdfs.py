from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import os

def create_pdf(filename, content):
    """Create a PDF file with the given content"""
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    doc = SimpleDocTemplate(f"data/{filename}", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom style
    custom_style = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
    )
    
    # Split content by lines and add to story
    for line in content.split('\n'):
        if line.strip():  # Skip empty lines
            story.append(Paragraph(line, custom_style))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"Created: data/{filename}")

# Create sample PDFs
handbook_content = """
Company Employee Handbook

Welcome to Our Company
We are excited to have you as part of our team. This handbook outlines our company policies, procedures, and expectations.

Work Hours
Standard work hours: 9:00 AM to 5:00 PM, Monday through Friday
Flexible scheduling available with manager approval
Remote work options for eligible positions

Leave Policies
Vacation Leave
Employees accrue 15 vacation days per year
Minimum 2 weeks notice required for planned leave
Maximum carryover: 5 days to next year

Sick Leave
10 sick days per year
Doctor's note required for absences exceeding 3 consecutive days

Benefits
Health Insurance
Medical, dental, and vision coverage
Company covers 80% of premium costs
Enrollment period: January 1-31 annually

Retirement Plan
401(k) with company match up to 4% of salary
Immediate eligibility for company match
"""

technical_content = """
Technical Development Guide

Development Standards
Code Quality
All code must pass code review before deployment
Unit test coverage should be at least 80%
Follow established naming conventions and patterns

Security Protocols
Regular security audits quarterly
All APIs must implement rate limiting
Sensitive data must be encrypted at rest and in transit

Deployment Process
Staging Environment
All features must be tested in staging for 48 hours
Performance testing required for high-traffic features
Database migrations must be backward compatible

Production Deployment
Deployments occur every Tuesday and Thursday
Rollback plan must be documented for each deployment
Monitoring alerts must be configured for new services

API Documentation Standards
All endpoints must have OpenAPI documentation
Include request/response examples
Document error codes and troubleshooting steps
"""

catalog_content = """
Product Catalog 2024

Software Products
Enterprise Suite
Price: $10,000 per year
Features: Advanced analytics, Custom reporting, API access
Support: 24/7 dedicated support line
Users: Up to 500 concurrent users

Professional Edition
Price: $5,000 per year
Features: Standard analytics, Scheduled reports
Support: Business hours support
Users: Up to 100 concurrent users

Starter Package
Price: $1,200 per year
Features: Basic reporting, Email support
Users: Up to 10 concurrent users

Hardware Products
Server Rack X1
Price: $15,000
Specs: 48 cores, 256GB RAM, 10TB SSD
Warranty: 3 years on-site support

Workstation Pro
Price: $3,500
Specs: 16 cores, 64GB RAM, 2TB NVMe
Warranty: 2 years parts and labor
"""

if __name__ == "__main__":
    create_pdf("company_handbook.pdf", handbook_content)
    create_pdf("technical_guide.pdf", technical_content)
    create_pdf("product_catalog.pdf", catalog_content)
    print("All sample PDFs created successfully!")