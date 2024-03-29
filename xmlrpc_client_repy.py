# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### C:\Dropbox\uni\y1p2\dist\lab\demokit\xmlrpc_client.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

"""
<Program Name>
  xmlrpc_client.py

<Started>
  May 3, 2009

<Author>
  Michael Phan-Ba

<Purpose>
  Implements the client-side XML-RPC protocol.

"""


repyhelper.translate_and_import('urlparse.repy')
repyhelper.translate_and_import('httpretrieve.repy')
repyhelper.translate_and_import('xmlrpc_common.repy')


class xmlrpc_client_Client(object):
  """
  <Purpose>
    XML-RPC client implementation.

  <Side Effects>
    None.

  <Example Use>
    client = xmlrpc_client_Client("http://phpxmlrpc.sourceforge.net/server.php")
    print client.send_request("examples.getStateName", (1,))

  """


  USER_AGENT = "seattlelib/1.0.0"


  def __init__(self, url):
    """
    <Purpose>
      Create a new XML-RPC Client object to do RPC calls to the given
      server.

    <Arguments>
      url:
        A url containing the hostname, port, and path of the xmlrpc
        server. For example, "http://phpxmlrpc.soureforge.net/server.php".

    <Exceptions>
      None.

    """

    if not isinstance(url, (str, unicode)):
      raise ValueError("Invalid argument: url must be a URL string")

    urlcomponents = urlparse_urlsplit(url, "http", False)

    self.server_host = urlcomponents["hostname"]
    self.server_port = urlcomponents["port"] or 80
    self.server_path = urlcomponents["path"] or "/"
    if urlcomponents["query"]:
      self.server_path += "?" + urlcomponents["query"]

    if not self.server_host:
      raise ValueError("Invalid argument: url must have a valid host")


  def send_request(self, method_name, params, timeout=None):
    """
    <Purpose>
      Send a XML-RPC request to a XML-RPC server to do a RPC call.

    <Arguments>
      method_name:
        The method name.

      params:
        The method parameters.

    <Exceptions>
      socket.error on socket errors, including server timeouts.
      xmlrpc_common_Fault on a XML-RPC response fault.
      xmlrpc_common_XMLParseError on a XML-RPC structural parse error.
      xmlparse_XMLParseError on a general XML parse error.
      xmlrpc_common_ConnectionError on unexpected disconnects.
      xmlrpc_common_Timeout if the time limit is exceeded.

    <Side Effects>
      None.

    <Returns>
      The XML-RPC method return values.

    """

    starttime = getruntime()

    # Prepare the XML request.
    request_xml = xmlrpc_common_call2xml(method_name, params)

    response = httpretrieve_get_string("http://%s:%s%s" % (self.server_host, \
        self.server_port, self.server_path), postdata=request_xml, \
        timeout=timeout, httpheaders={\
        "User-Agent": self.USER_AGENT, "Content-Type": "text/xml"})

    # Timeout if the POST took too long.
    if timeout is not None and getruntime() - starttime > timeout:
      raise xmlrpc_common_Timeout()

    # Parse the XML response body into Python values.
    response_value = xmlrpc_common_response2python(response)

    # If a fault was decoded, raise the exception.
    if isinstance(response_value, xmlrpc_common_Fault):
      raise response_value

    # Otherwise, return the results.
    return response_value

### Automatically generated by repyhelper.py ### C:\Dropbox\uni\y1p2\dist\lab\demokit\xmlrpc_client.repy
