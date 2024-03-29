# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### C:\Dropbox\uni\y1p2\dist\lab\demokit\DORadvertise.repy

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
Author: Conrad Meyer

Start Date: Wed Dec 9 2009

Description:
Advertisements to the Digital Object Registry run by CNRI.

"""




repyhelper.translate_and_import('sockettimeout.repy')
repyhelper.translate_and_import('httpretrieve.repy')
repyhelper.translate_and_import('xmlparse.repy')




DORadvertise_FORM_LOCATION = "http://geni.doregistry.org/SeattleGENI/HashTable"




class DORadvertise_XMLError(Exception):
  """
  Exception raised when the XML recieved from the Digital Object Registry
  server does not match the structure we expect.
  """
  pass




class DORadvertise_BadRequest(Exception):
  """
  Exception raised when the Digital Object Registry interface indigates we
  have made an invalid request.
  """


  def __init__(self, errno, errstring):
    self.errno = errno
    self.errstring = errstring
    Exception.__init__(self, "Bad DOR request (%s): '%s'" % (str(errno), errstring))




def DORadvertise_announce(key, value, ttlval, timeout=None):
  """
  <Purpose>
    Announce a (key, value) pair to the Digital Object Registry.

  <Arguments>
    key:
            The new key the value should be stored under.

    value:
            The value to associate with the given key.

    ttlval:
            The length of time (in seconds) to persist this key <-> value
            association in DHT.

    timeout:
            The number of seconds to spend on this operation before failing
            early.

  <Exceptions>
    xmlparse_XMLParseError if the xml returned isn't parseable by xmlparse.
    DORadvertise_XMLError if the xml response structure does not correspond
      to what we expect.
    DORadvertise_BadRequest if the response indicates an error.
    Any exception httpretrieve_get_string() throws (including timeout errors).

  <Side Effects>
    The key <-> value association gets stored in openDHT for a while.

  <Returns>
    None.
  """

  post_params = {'command': 'announce', 'key': key, 'value': value,
      'lifetime': str(int(ttlval))}

  _DORadvertise_command(post_params, timeout=timeout)

  return None





def DORadvertise_lookup(key, maxvals=100, timeout=None):
  """
  <Purpose>
    Retrieve a stored value from the Digital Object Registry.

  <Arguments>
    key:
            The key the value is stored under.

    maxvals:
            The maximum number of values stored under this key to
            return to the caller.

    timeout:
            The number of seconds to spend on this operation before failing
            early.   If not specified, the default is set to the default
            timeout value for the http library (30 seconds).

  <Exceptions>
    xmlparse_XMLParseError if the xml returned isn't parseable by xmlparse.
    DORadvertise_XMLError if the xml response structure does not correspond
      to what we expect.
    DORadvertise_BadRequest if the response indicates an error.
    Any exception httpretrieve_get_string() throws (including timeout errors).

  <Side Effects>
    None.

  <Returns>
    The value stored in the Digital Object Registry at key.
  """

  post_params = {'command': 'lookup', 'key': key, 'maxvals': str(maxvals)}

  return _DORadvertise_command(post_params, timeout=timeout)



def _DORadvertise_command(parameters, timeout=None):
  # Internal helper function; calls the remote command, and returns
  # the results we can glean from it.

  # If there is a timeout, use it!
  if timeout != None:
    post_result = httpretrieve_get_string(DORadvertise_FORM_LOCATION, \
        postdata=parameters, timeout=timeout, \
        httpheaders={"Content-Type": "application/x-www-form-urlencoded"})
  else:
    post_result = httpretrieve_get_string(DORadvertise_FORM_LOCATION, \
        postdata=parameters, \
        httpheaders={"Content-Type": "application/x-www-form-urlencoded"})


  # Parse the result to check for success. Throw several exceptions to
  # ensure the XML we're reading makes sense.
  xmltree = xmlparse_parse(post_result)

  if xmltree.tag_name != "HashTableService":
    raise DORadvertise_XMLError(
        "Root node error. Expected: 'HashTableService', " +
        "got: '%s'" % xmltree.tag_name)

  if xmltree.children is None:
    raise DORadvertise_XMLError("Root node contains no children nodes.")

  # We expect to get an error code, an error string, and possibly some
  # values from the server.
  error_msg = None
  error = None
  values = None

  numxmlchildren = len(xmltree.children)
  if numxmlchildren not in [2, 3]:
    raise DORadvertise_XMLError("Root XML node contains inappropriate " + \
        "number of child nodes.")

  for xmlchild in xmltree.children:
    # Read the numeric error code.
    if xmlchild.tag_name == "status" and xmlchild.content is not None:
      if error is not None:
        raise DORadvertise_XMLError("XML contains multiple status tags")
      error = int(xmlchild.content.strip())

    # String error message (description:status as strerror:errno).
    elif xmlchild.tag_name == "description":
      if error_msg is not None:
        raise DORadvertise_XMLError("XML contains multiple description tags")
      error_msg = xmlchild.content

    # We found a <values> tag. Let's try and get some values.
    elif xmlchild.tag_name == "values" and xmlchild.children is not None:
      if values is not None:
        raise DORadvertise_XMLError("XML contains multiple values tags")

      values = []
      for valuenode in xmlchild.children:
        if valuenode.tag_name != "value":
          raise DORadvertise_XMLError(
              "Child tag of <values>; expected: '<value>', got: '<%s>'" % \
                  valuenode.tag_name)

        content = valuenode.content
        if content is None:
          content = ""

        values.append(content)

    # Check for tags we do not expect.
    elif xmlchild.tag_name not in ("status", "description", "values"):
      raise DORadvertise_XMLError("Unexpected tag '" + \
          str(xmlchild.tag_name) + "' while parsing response.")

  if error is not 0:
    raise DORadvertise_BadRequest(error, error_msg)

  # This happens when the server returns <values></values>
  if values is None:
    return []

  return values

### Automatically generated by repyhelper.py ### C:\Dropbox\uni\y1p2\dist\lab\demokit\DORadvertise.repy
