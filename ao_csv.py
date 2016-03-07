# -*- coding: utf8 -*-
import base64
import csv,codecs,cStringIO
import datetime
from StringIO import StringIO

def csv_to_list(data_file,source_encoding = "utf_8"):
    
    # to detect delimiter on the fly        
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(data_file, delimiters=',;')
    reader  = UnicodeReader(StringIO(data_file), dialect=dialect,encoding=source_encoding)
 
    items    = {}
    row_model= {}

    if reader.reader:
        col_fields = reader.header
        col_max    = len(col_fields)
        for numcol in range(0,col_max-1):
            row_model[numcol] = ''
    
        row_number = 0
        for row in reader.reader:
            numcol= 0 
            for col in row:
                if numcol<col_max: 
                    value = row[numcol].strip()
                    
                    if items.has_key(row_number):
                        row_value = items[row_number]
                    else:
                        row_value = row_model.copy()
                    
                    row_value[numcol] = value
                    items[row_number] = row_value
                numcol +=1 
            row_number +=1
        
    return list(items.values())

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, source_encoding):
        self.source_encoding = source_encoding
        self.target_encoding = 'utf_8'
        self.state = False
        try:
            self.reader = codecs.getreader(self.source_encoding)(f)
            self.state = True
        
        except UnicodeEncodeError:
            self.state = False
                
        except UnicodeDecodeError:
            self.state = False
            
    def __iter__(self):
        return self

    def next2(self):
        return self.reader.next().encode(self.target_encoding)

    def next(self):
        try:
            conv = self.reader.next().encode(self.target_encoding)
        except UnicodeEncodeError:
            conv = 'Encoding Error'   
        return conv 

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect, encoding, **kwds):
        self.source_encoding = encoding
        self.target_encoding = 'utf_8'
        f = UTF8Recoder(f, self.source_encoding)
        if f.state:
            self.reader = csv.reader(f, dialect=dialect, **kwds)
            self.header = self.next()
        else:
            self.reader = False
            
    def next(self,format_dic = False):
        row = self.reader.next()
        vals = [unicode(s, self.target_encoding) for s in row]
        if format_dic:
            return dict((self.header[x], vals[x]) for x in range(len(self.header))) 
        else:
            return vals
     
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.fieldnames = fieldnames
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writeheader(self):
        self.writer.writerow(self.fieldnames)

    def writerow(self, row):
        self.writer.writerow([row[x].encode("utf-8") for x in self.fieldnames])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
 

class migrate_luncher(object):    

    def __init__(self,cr,uid,pool,filepath):
        self.cr = cr
        self.uid = uid
        self.pool = pool
        model_ref = dict()
        filepath = ''

    def migrate_execute(self, cr, uid, ids, context=None):
        mydir =  'openerp/addons/payroll_AgilOrg/data/'
        self.process_migrate(mydir,cr,uid)
        
    def process_migrate(self,filepath,cr,uid):
        self.filepath = filepath
        self.del_table('my_table')
      
    def del_table(self,name):
        self.cr.execute("delete from " + name + " cascade ")
  
    def get_model_key_id(self,model,record_key):
        if self.model_ref.has_key(record_key) is True:
            my_dict = self.model_ref[record_key]
            return my_dict['id']
        else:
            print model,record_key,'inexistant'
    
    def set_model_key(self,model,record_key,record):
        if self.model_ref.has_key(record_key)== False:
            self.model_ref[record_key] = record
        else:
            print 'Doublon',model
            print record_key,record
    
    def find_record_id(self,model,domain):
        print 'find record : ',model,domain
        obj_pool = self.pool.get(model)
        ids = obj_pool.search(cr, uid, domain)  
        #res = obj.read(cr, uid, ids, ['name', 'id'], context)  
        print 'find record : ',model,domain,ids     
        if ids:
            return ids[0]
        else:
            return None
    
    def str_to_int(self,rubrique_code):
        try:
            x = int(rubrique_code)
        except ValueError:
            x = 0
            
        return x
    
            
    def import_model(self,attributes):
        
        model    = attributes.get('model', default=None)
        csv_file = attributes.get('csv_file', default=None)
        key_list = attributes.get('key_list', default=[])
        print 'import_for model',model
        model_pool = self.pool.get(model)
        my_file = open(self.filepath + csv_file, "rb")
        try:
            reader = csv.reader(my_file)
            lst_fields = reader.next()
            print fields 
            
            for row in reader:
                col = 0
                record = {} 
                for field in lst_fields:
                    field_name = field.strip() 
                    if field_name:
                        record[field_name] = row[col] 
                    col = col+1
                    
                record_key = []
                for key in key_list:
                    record_key.append(record[key])
                        
                record_id = model_pool.create(cr, uid,record)
                record['id'] = record_id
                self.set_model_key(model,record_key,record)
                
                
        finally:
            my_file.close()
            
class fs_csv_import(object):
    
    def __init__(self,source_path,target_path,sep=';'):
        self.source_path = source_path
        self.target_path = target_path
        self.sep = sep;
        
    def open_source(self,key_col,file_name):
        source = fs_csv_file(key_col,[],self.sep,self.source_path,file_name)
        return source
        
    def open_target(self,key_col,cols):
        target = fs_csv_file(key_col,cols,self.sep)
        return target 
    
    def export(self,script,source,target):
        for key,row in source.values.items():
            newline = target.new_row()
            for new_field,field in script:
                value = source.get_value(row,field)
                target.set_value(newline, new_field,value)
                target.add_row(newline)
        return target 
    
    def target_write(self,target,filename,sep=';'):        
        target.write(self.target_path,filename,sep)
        

class ao_csv_file(object):
    
    def __init__(self,key_cols,cols=[],sep=';',filepath=None,file_name=None):
        if filepath == None or file_name == None:
            self.create_newcsv(key_cols,cols,sep)
        else:
            self.read_csvfile(filepath,file_name,key_cols,sep=';')
            
    def target_path(self,target):
        self.target_path(target)
        
    def create_newcsv(self,key_cols,cols,sep=';'):
        self.values = {}
        self.cols   = cols
        self.key_cols = key_cols
       
    def read_csvfile(self,filepath,file_name,key_cols,sep=';'):
        self.values = {}
        self.cols = []
        self.key_cols = key_cols
        
        my_file = open(filepath + file_name, "rb")
        try:
            reader = csv.reader(my_file,delimiter=sep)
            self.cols = list(reader.next()) 
            for row in reader:
                myrow = list(row)
                self.add_row(myrow)
        finally:
            my_file.close()                     

    def conv_date(self,my_date):
        year  = int(my_date[6:10])
        month = int(my_date[3:5])
        day   = int(my_date[0:2])
        if year==0: 
            year = 2014
        if month==0:
            month=1
        if day==0:
            day=1
        print 'my_date : ',my_date,year,month,day
        return datetime.date(year,month, day)
    
    def new_row(self):
        row = list()
        for i in range(len(self.cols)):
            row.append('')
        return row
    
    def add_row(self,row):
        key = self.get_key(row)
        self.values[key] = row
            
        
    def get_key(self,row):
        key = ''
        for colname in self.key_cols:
            index = self.cols.index(colname)
            key = key + self.get_value(row,colname)
        return key
    
    def is_key(self,key,colname):
        if self.values.has_key(key):
            return True
        else:
            return False
        
    def get_search_value(self,key,colname):
        if self.values.has_key(key):
            row = self.values[key]
            return self.get_value(row,colname)
        
    def get_value(self,row,colname,format='string'):
        ret_val = ''
        index = self.cols.index(colname)
        if len(row)> index:
            ret_val = row[index] 
        
        if format=='date':
            ret_val = self.conv_date(ret_val)
        return ret_val
    
    def set_value(self,row,colname,value,format='string'):
        if format == 'date':
            value = self.conv_date(value)
        if colname in self.cols:
            index = self.cols.index(colname)
            if len(row)> index:
                row[index] = value
            else:
                row.insert(index,value)
                
    def set_value_all(self,colname,value,format='string'):
        index = self.cols.index(colname)
        for key,row in self.values.items():
            if format=='date':
                row[index] = self.conv_date(value)  
            else: 
                row[index] = value 
    
    def replace_value_all(self,colname,old_value,new_value):
        index = self.cols.index(colname)
        for key,row in self.values.items():
            if row[index].strip() == old_value:
                row[index] = new_value
                
    def check_value_all(self,colname,lst_value,def_value):
        index = self.cols.index(colname)
        for key,row in self.values.items():
            if not(row[index].strip() in lst_value):
                row[index] = def_value             
    
    def delete_field(self,colname):
        if colname in self.cols:
            index = self.cols.index(colname)
            for key,row in self.values.items():
                del row[index]
            self.cols.remove(colname)
                 
    def add_field(self,colname,def_value):
        if not (colname in self.cols):
            self.cols.append(colname)
            index = self.cols.index(colname)
            for key,row in self.values.items():
                row.insert(index,def_value)
                
    def write(self,filepath,file_name,sep=';'):
        
        with open(filepath+file_name, 'wb') as csvfile:
            newcsv = csv.writer(csvfile, delimiter=sep)
            newcsv.writerow(self.cols)
            for key,row in self.values.items():
                newcsv.writerow(row)

    def print_values(self):
        for row in self.values.items():
            print row 
    

