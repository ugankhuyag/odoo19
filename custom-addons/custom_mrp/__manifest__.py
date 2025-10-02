{
    'name': 'Custom MRP',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Custom Manufacturing Extensions',
    'description': """
        Custom Manufacturing Module
        ===========================
        This module extends the standard MRP functionality with:
        - Custom fields
        - Custom reports
        - Custom workflows
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'images': ['static/description/icon.png'],
    'depends': [
        'base',
        'purchase',
        'mrp',
        'purchase_stock',
        'sale_mrp',
    ],
    'data': [
        'views/mrp_production_views.xml',
        'security/mrp_security.xml',
        # 'security/ir.model.access.csv',
        # 'data/custom_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
