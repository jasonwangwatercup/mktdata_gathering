# -*- coding: utf-8 -*-

# %[p][m[.n]]c
# p: format codes prefix, in ('+','-','0','#');
# m: integer specifying total desired width, (negative means left-aligned??);
# n: integer spedifying the number of digits after the decimal point;
# c: indicating the type of formatting, in ("s","d","e","E","f","g","G","o","x","X","c","%")

# min_len: the maximum between length of a name(name_compact) and the given reasonable minimum length of such a name.
# myfield: (name, name_compact, min_len). 
# print_fields_format: the proper formats for printing for a list of myfield, compact or not.
# isinstance() is usually the preferred way to ensure the type of an object because it will also accept derived types.

# print_list_formatted()

import types
import pdb


class myfield(object):
    def __init__(self, name, name_compact, min_len,p=None,n=None,c='s',dpcnt=False):
        if isinstance(name, types.StringTypes) is True:
            self.__name = name.strip()
        else:
            print "name must be StringTypes: PAUSED and return."
            pdb.set_trace()
            return
        if isinstance(name_compact, types.StringTypes) is True:
            self.__name_compact = name_compact.strip()
        else:
            print "name_compact must be StringTypes: PAUSED and return."
            pdb.set_trace()
            return
        if 0 >= min_len:
            print "min_len must be positive. PAUSED and return."
            pdb.set_trace()
            return
        else:
            min_len = int(min_len)
            self.__min_len = max(min_len, len(self.__name))
            self.__min_len_compact = max(min_len, len(self.__name_compact))
            self.__ml = min_len
        self.__print_format = '%'
        self.__print_fmt_cmpct = '%'
        self.__formats = (p,n,c,dpcnt)
        if p is not None:
            p = p.strip()
            if p not in ('+','-','0','#'):
                print "p should be in ('+','-','0','#').PAUSED&return."
                pdb.set_trace()
                return
            else:
                self.__print_format = self.__print_format + p
                self.__print_fmt_cmpct = self.__print_fmt_cmpct + p
        self.__print_format = self.__print_format + str(self.__min_len)
        self.__print_fmt_cmpct = self.__print_fmt_cmpct + str(self.__min_len_compact)
        if n is not None:
            n = int(n)
            if 0 >= n:
                print "n should be positive. PAUSED&return."
                pdb.set_trace()
                return
            else:
                self.__print_format = self.__print_format+'.'+str(n)
                self.__print_fmt_cmpct = self.__print_fmt_cmpct+'.'+str(n)
        if c is not None:
            c = c.strip()
            if c not in ("s","d","e","E","f","g","G","o","x","X","c"):
                print """c should be in ("s","d","e","E","f","g","G","o","x","X","c"). PAUSED&return."""
                pdb.set_trace()
                return
            else:
                self.__print_format = self.__print_format + c
                self.__print_fmt_cmpct = self.__print_fmt_cmpct + c
        if dpcnt is True:
            self.__print_format = self.__print_format + '%%'
            self.__print_fmt_cmpct = self.__print_fmt_cmpct + '%%'
            

    def get_name(self):
        return self.__name

    def get_name_compact(self):
        return self.__name_compact

    def get_min_len(self):
        return self.__min_len

    def get_min_len_compact(self):
        return self.__min_len_compact

    def get_ml(self):
        return self.__ml

    def get_print_format(self):
        return self.__print_format

    def get_print_fmtcmpct(self):
        return self.__print_fmt_cmpct

    def get_format_parameters(self):
        return self.__formats


class myfield_0(myfield):
    def __init__(self, m_field):
        if isinstance(m_field, myfield) is True:
            tmp1 = m_field.get_format_parameters()
            myfield.__init__(self, m_field.get_name()+'_0', m_field.get_name_compact()+'_0', m_field.get_ml(), tmp1[0], tmp1[1], tmp1[2], tmp1[3])
        else:
            print "myfield_0 should be derived from myfield: PAUSED and return."
            pdb.set_trace()
            return
           

class print_fields_format(object):
    def __init__(self, list_fields, printYN=False):
        tmp = map(lambda x: isinstance(x, myfield), list_fields)
        if len(list_fields) > sum(tmp):
            print "all elements of the list SHOULD be of type field. PAUSED and return.."
            for i in xrange(len(list_fields)):
                if tmp[i] is False:
                    print "%s of list_fields is not of type myfield." % i
            pdb.set_trace()
            return
        self.__fields = tuple(map(lambda x: x.get_name(), list_fields))
        self.__fields_compact = tuple(map(lambda x: x.get_name_compact(), list_fields))
        self.__format_print = '|'.join(map(lambda x: x.get_print_format(), list_fields))
        self.__format_print_compact = '|'.join(map(lambda x: str(x.get_print_fmtcmpct()), list_fields))

        if printYN is True:
            print self.__fields
            print self.__fields_compact
            print self.__format_print
            print self.__format_print_compact
            print "and the cases for the original list:"
            print map(lambda x: x.get_min_len(), list_fields)
            print map(lambda x: x.get_min_len_compact(), list_fields)
            
            print "now test printing:"
            print self.__format_print % self.__fields
            print self.__format_print_compact % self.__fields_compact

    def get_fields(self):
        return self.__fields

    def get_fields_compact(self):
        return self.__fields_compact

    def get_format_print(self):
        return self.__format_print

    def get_format_print_compact(self):
        return self.__format_print_compact


def print_list_formatted(p_fields, lst, logger=None, b_compact=True):
    try:
        ee = print_fields_format(p_fields)
    except Exception as e:
        print "print_fields_format error!%s. PAUSED." % e.args[0]
        pdb.set_trace()
    else:
        if 0 == len(lst):
            print "lst is []. PAUSED"
            pdb.set_trace()
        else:
            if b_compact is True:
                print ee.get_format_print_compact() % ee.get_fields_compact() 
                try:
                    print ee.get_format_print_compact() % lst[0]
                except Exception as e:
                    print "print_fields_format error!%s. PAUSED." % e.args[0]
                    pdb.set_trace()
                else:
                    for i in lst[1:]:
                        print ee.get_format_print_compact() % i
                    if logger is not None:
                        for i in lst:
                            logger.debug(ee.get_format_print_compact() % i)
            else:
                print ee.get_format_print() % ee.get_fields()
                try:
                    print ee.get_format_print() % lst[0]
                except Exception as e:
                    print "print_fields_format error!%s. PAUSED." % e.args[0]
                    pdb.set_trace()
                else:
                    for i in lst[1:]:
                        print ee.get_format_print() % i
                    if logger is not None:
                        for i in lst:
                            logger.debug(ee.get_format_print() % i)
