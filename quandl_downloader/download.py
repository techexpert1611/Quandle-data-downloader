# GET https://www.quandl.com/api/v3/datasets/{database_code}/{dataset_code}/data.{return_format}
import requests
import json
import os
import xml.dom.minidom


def download_to_file(url, filename, file_dir='downloaded_data/'):
    """
    Downloads and saves file to given path.

    :param url: url for the quandl dataset api.
    :param filename: name of the file.
    :param file_dir: (optional) path to the directory where you want to save file.
    :return: boolean telling whether file was saved or not

    url must be in below given form:
    https://www.quandl.com/api/v3/datasets/{database_code}/{dataset_code}/data.{return_format}?api_key={api_key}
    """
    file_dir.replace('\\', '/')
    file_dir += '/'
    if file_dir == 'downloaded_data/' or os.path.exists(file_dir):
        if url == '':
            raise ValueError('URL can not be null')

        elif filename == '':
            raise ValueError('Filename can not be null')

        file_format = url.split('?')[0].split('.')[-1]
        try:
            data = requests.get(url)
        except Exception as e:
            print(str(e))
            return False

        if file_format == 'json':
            if os.path.isfile(file_dir + filename + '.json'):
                print(file_dir)
                raise FileExistsError('File with same name already exists, if you want to override delete it first.')
            try:
                data = data.json()
                data = json.dumps(data)
                parsed_data = json.loads(data)
            except:
                print('your url did not return a valid json response')
                return False

            try:
                with open(file_dir + filename + '.json', 'w') as outfile:
                    json.dump(parsed_data, outfile, indent=4)
                return True
            except FileNotFoundError as e:
                print(str(e))
                return False
            except EOFError as e:
                print(str(e))
                return False

        elif file_format == 'xml':

            if os.path.isfile(file_dir + filename + '.xml'):
                raise FileExistsError('File with same name already exists, if you want to override delete it first.')

            try:
                tree = xml.dom.minidom.parseString(data.content)
                pretty = tree.toprettyxml()

            except:
                print('your url did not return a valid  xml response')
                return False

            try:
                with open(file_dir + filename + '.xml', 'w') as outfile:
                    outfile.write(pretty)
                return True
            except FileNotFoundError as e:
                print(str(e))
                return False

            except EOFError as e:
                print(str(e))
                return False

        elif file_format == 'csv':
            if os.path.isfile(file_dir + filename + '.csv'):
                raise FileExistsError('File with same name already exists, if you want to override delete it first.')

            try:
                open(file_dir + filename + '.csv', 'wb').write(data.content)
                return True
            except FileNotFoundError as e:
                print(str(e))
                return False
            except EOFError as e:
                print(str(e))
                return False
    else:
        raise FileNotFoundError


# download_to_file('https://www.quandl.com/api/v3/datasets/WIKI/FB/data.json?api_key=your_key_here', 'test', file_dir="test")