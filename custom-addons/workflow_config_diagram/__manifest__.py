{
    'name': 'workflow config diagram',
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
        'security/workflow_config_security.xml',
        'views/workflow_config_views.xml',
        #
        # 'data/ir_cron.xml'

        # 'security/ir.model.access.csv',
        # 'data/custom_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
