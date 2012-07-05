from django.template import Library
from django.core.urlresolvers import reverse

from django.conf import settings

import r66.models

menu = {}
menu["home"] = ["interfaces", "bridges", "search", "ppp3g", "success"]
menu["about"] = []
menu["bridges"] = ["bridge_profiles"]
menu["interfaces"] = ["interface_profiles"]
menu["contact"] = []

register = Library()

def if_equal_res(val1,val2,res_true,res_false):
    if val1 == val2:
        return res_true
    else:
        return res_false

def if_page_in_menu (page_id, menu_id):
  try:
    menu[menu_id].index(page_id)
    return True
  except ValueError:
    return False


def render_nav_menu(page_id):

    def _aux_active_class (page_id,menu_id):
       return 'class="active"' if if_page_in_menu(page_id, menu_id) else ""

    _menu = '''
          <div class="nav-collapse">
            <ul class="nav">
                <li ''' \
                + _aux_active_class(page_id,"home") \
                + ''' > <a href="''' + reverse('r66-home',args=["interfaces"]) \
                + '''">Home</a></li> '''

    ns = r66.models.NetIface.objects.all()
    if len (r66.models.NetIface.objects.all() ) > 0:
        any_enabled = False
        for n in ns:
            if n.enabled == True:
                any_enabled = True
                break
        if any_enabled:
            _menu = _menu + '''<li ''' \
                + _aux_active_class(page_id,"interfaces") \
                + ''' > ''' \
                + '''<a href="''' \
                + reverse('r66-interfaces-index',args=None) \
                + '''">Interfaces</a></li> '''

    if len (r66.models.NetBridge.objects.all() ) > 0:
        _menu = _menu + '''<li ''' \
                + _aux_active_class(page_id,"bridges") \
                + ''' > <a href="''' + reverse('r66-bridges',args=None) \
                + '''">Bridges</a></li> '''

    _menu = _menu + ''' <li ''' \
                + _aux_active_class(page_id,"about") \
                + ''' ><a href="#about">About</a></li>
                <li ''' \
                + _aux_active_class(page_id,"contact") \
                + ''' ><a href="#contact">Contact</a></li>
            </ul>
          </div><!--/.nav-collapse -->'''

    return _menu

register.simple_tag(render_nav_menu)

def render_home_menu(page_id):

    _menu = '''
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Devices</li>
                <li ''' \
                + if_equal_res(page_id, "interfaces",'class="active"','') \
                + ''' > <a href="''' + reverse('r66-home',args=["interfaces"]) \
                + '''">Interfaces</a></li>
                <li ''' \
                + if_equal_res(page_id, "bridges",'class="active"','') \
                + ''' > <a href="''' + reverse('r66-home',args=["bridges"]) \
                + '''">Bridges</a></li>
                <li ''' \
                + if_equal_res(page_id, "ppp3g",'class="active"','') \
                + ''' > <a href="''' + reverse('r66-home',args=["ppp3g"]) \
                + '''">PPP/3G</a></li>
              <li class="nav-header">Search</li>
                <li ''' \
                + if_equal_res(page_id, "search",'class="active"','') \
                + ''' > <a href="''' + reverse('r66-home',args=["search"]) \
                + '''">Search network devices</a></li>
            </ul>
          </div><!--/.well -->'''

    return _menu

    # if isinstance (node, int):
    #   node = models.Component.objects.get(pk=node)
    # res = '<a href="' + reverse('fileclusters-node',args=[node.id]) + '">' + node.__unicode__() + '</a>'

    # res = helpers._binding_templatetags_hooks ("node_item", res, node)

    # if node.master:
    #   res = res + "<strong> (master node) </strong>"
    # return res

register.simple_tag(render_home_menu)


