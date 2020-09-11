"""
OLITT WHMCS
"""


class Product:
    """This object contains a whmcs product."""

    def __init__(self, whmcs_product):
        print(whmcs_product)
        self.id = whmcs_product.get('pid')


"""
Example response
{
    "result": "success",
    "totalresults": 4,
    "products": {
        "product": [
            {
                "pid": 92,
                "gid": 4,
                "type": "other",
                "name": "Lifetime Account",
                "description": "Free Olitt.com Domain<br /> \r\nConnect  Custom Domain<br /> \r\nNo Olitt.com Branding<br /> \r\nSSL certificate<br />\r\nSEO Friendly<br />\r\nDNS Management<br />\r\nPre-built Websites<br />\r\n5GB Disk Space<br />\r\nExternal Integrations<br />\r\nPriority Support<br />\r\n3 Websites Package<br /> ",
                "module": "",
                "paytype": "onetime",
                "pricing": {
                    "CNY": {
                        "prefix": "¥",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "677.64",
                        "quarterly": "164.28",
                        "semiannually": "328.55",
                        "annually": "657.10",
                        "biennially": "1314.20",
                        "triennially": "2628.41"
                    },
                    "EUR": {
                        "prefix": "€",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "84.09",
                        "quarterly": "20.39",
                        "semiannually": "40.77",
                        "annually": "81.54",
                        "biennially": "163.08",
                        "triennially": "326.17"
                    },
                    "INR": {
                        "prefix": "INR",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "7282.80",
                        "quarterly": "1765.53",
                        "semiannually": "3531.06",
                        "annually": "7062.11",
                        "biennially": "14124.22",
                        "triennially": "28248.45"
                    },
                    "KES": {
                        "prefix": "KES ",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "9900.00",
                        "quarterly": "2400.00",
                        "semiannually": "4800.00",
                        "annually": "9600.00",
                        "biennially": "19200.00",
                        "triennially": "38400.00"
                    },
                    "USD": {
                        "prefix": "$",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "99.00",
                        "quarterly": "24.00",
                        "semiannually": "48.00",
                        "annually": "96.00",
                        "biennially": "192.00",
                        "triennially": "384.00"
                    },
                    "ZAR": {
                        "prefix": "R",
                        "suffix": "",
                        "msetupfee": "0.00",
                        "qsetupfee": "0.00",
                        "ssetupfee": "0.00",
                        "asetupfee": "0.00",
                        "bsetupfee": "0.00",
                        "tsetupfee": "0.00",
                        "monthly": "1656.96",
                        "quarterly": "401.69",
                        "semiannually": "803.37",
                        "annually": "1606.75",
                        "biennially": "3213.49",
                        "triennially": "6426.98"
                    }
                },
                "customfields": {
                    "customfield": []
                },
                "configoptions": {
                    "configoption": []
                }
            }
        ]
    }
}
"""
