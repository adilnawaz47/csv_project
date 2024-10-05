# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# import json
# import re

# # View to render the JSON comparison page
# def compare_json(request):
#     return render(request, 'compare_json.html')

# # Function to compare two JSON objects
# def compare_json_objects(json1, json2, path=""):
#     """Recursively compares two JSON objects and returns a list of differences."""
#     differences = []

#     if isinstance(json1, dict) and isinstance(json2, dict):
#         all_keys = set(json1.keys()).union(set(json2.keys()))

#         for key in all_keys:
#             new_path = f"{path}.{key}" if path else key
#             if key not in json1:
#                 differences.append({'path': new_path, 'type': 'missing', 'value': json2[key]})
#             elif key not in json2:
#                 differences.append({'path': new_path, 'type': 'missing', 'value': json1[key]})
#             else:
#                 # Check if the values are different
#                 if json1[key] != json2[key]:
#                     differences.append({'path': new_path, 'type': 'diff', 'value1': json1[key], 'value2': json2[key]})
#                 else:
#                     # If values are the same, continue deeper comparison
#                     differences.extend(compare_json_objects(json1[key], json2[key], new_path))

#     elif isinstance(json1, list) and isinstance(json2, list):
#         len1, len2 = len(json1), len(json2)
#         max_length = max(len1, len2)

#         for i in range(max_length):
#             new_path = f"{path}[{i}]"
#             if i >= len1:
#                 differences.append({'path': new_path, 'type': 'missing', 'value': json2[i]})
#             elif i >= len2:
#                 differences.append({'path': new_path, 'type': 'missing', 'value': json1[i]})
#             else:
#                 # Check if the values are different
#                 if json1[i] != json2[i]:
#                     differences.append({'path': new_path, 'type': 'diff', 'value1': json1[i], 'value2': json2[i]})

#     else:
#         # Compare values directly if neither is a dict or list
#         if json1 != json2:
#             differences.append({'path': path, 'type': 'diff', 'value1': json1, 'value2': json2})

#     return differences


# def compare_json_ajax(request):
#     try:
#         # Load JSON from POST request
#         json_obj1 = json.loads(request.POST.get('json_obj1'))
#         json_obj2 = json.loads(request.POST.get('json_obj2'))

#         # Compare the JSON objects
#         differences = compare_json_objects(json_obj1, json_obj2)

#         # Generate HTML with colored differences
#         html_json1, html_json2 = generate_html_with_differences(json_obj1, json_obj2, differences)

#         # Return the HTML response
#         response = JsonResponse({'status': 'True', 'html_json1': html_json1, 'html_json2': html_json2})
#     except json.JSONDecodeError as e:
#         response = JsonResponse({'status': 'false', 'message': f"Invalid JSON data: {str(e)}"})
#     except Exception as e:
#         response = JsonResponse({'status': 'false', 'message': str(e)})

#     return response

# def generate_html_with_differences(json1, json2, differences):
#     """Generates HTML representation of JSON with highlighted differences."""
#     html_json1 = prettify_json(json.dumps(json1))  # Prettify JSON1
#     html_json2 = prettify_json(json.dumps(json2))  # Prettify JSON2

#     # Apply differences
#     for diff in differences:
#         path = diff['path']
#         highlight_class = 'highlight-missing' if diff['type'] == 'missing' else 'highlight-diff'
        
#         # Highlight JSON 1
#         html_json1 = highlight_json(html_json1, path, highlight_class)

#         # Highlight JSON 2
#         if diff['type'] == 'diff':
#             html_json2 = highlight_json(html_json2, path, highlight_class)

#     return html_json1, html_json2

# def prettify_json(json_str):
#     """Format JSON string for pretty display."""
#     return json.dumps(json.loads(json_str), indent=4, separators=(',', ': ')).replace(' ', '&nbsp;').replace('\n', '<br/>')


# def highlight_json(json_str, path, highlight_class):
#     """Highlights the given path in the JSON string with the specified CSS class."""
#     # Adjust path formatting for regex
#     escaped_path = path.replace('.', r'\.').replace('[', r'\[').replace(']', r'\]')
#     regex = r'("(' + escaped_path + r')":?)'

#     # Use HTML span tags to highlight
#     return re.sub(regex, r'<span class="' + highlight_class + r'">\1</span>', json_str)














from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import re

# View to render the JSON comparison page
def compare_json(request):
    return render(request, 'compare_json.html')

# Function to compare two JSON objects
def compare_json_objects(json1, json2, path=""):
    """Recursively compares two JSON objects and returns a list of differences."""
    differences = []

    if isinstance(json1, dict) and isinstance(json2, dict):
        all_keys = set(json1.keys()).union(set(json2.keys()))

        for key in all_keys:
            new_path = f"{path}.{key}" if path else key
            if key not in json1:
                # Key is missing in json1 (added in json2)
                differences.append({'path': new_path, 'type': 'added', 'value': json2[key]})
                if isinstance(json2[key], dict):
                    for sub_key in json2[key].keys():
                        differences.append({'path': f"{new_path}.{sub_key}", 'type': 'added_value', 'value': json2[key][sub_key]})
                elif isinstance(json2[key], list):
                    for index, item in enumerate(json2[key]):
                        differences.append({'path': f"{new_path}[{index}]", 'type': 'added_value', 'value': item})
            elif key not in json2:
                # Key is missing in json2 (removed from json1)
                differences.append({'path': new_path, 'type': 'removed', 'value': json1[key]})
                if isinstance(json1[key], dict):
                    for sub_key in json1[key].keys():
                        differences.append({'path': f"{new_path}.{sub_key}", 'type': 'removed_value', 'value': json1[key][sub_key]})
                elif isinstance(json1[key], list):
                    for index, item in enumerate(json1[key]):
                        differences.append({'path': f"{new_path}[{index}]", 'type': 'removed_value', 'value': item})
            else:
                # Check if the values are different
                if json1[key] != json2[key]:
                    differences.append({'path': new_path, 'type': 'diff', 'value1': json1[key], 'value2': json2[key]})
                else:
                    # If values are the same, continue deeper comparison
                    differences.extend(compare_json_objects(json1[key], json2[key], new_path))

    elif isinstance(json1, list) and isinstance(json2, list):
        len1, len2 = len(json1), len(json2)
        max_length = max(len1, len2)

        for i in range(max_length):
            new_path = f"{path}[{i}]"
            if i >= len1:
                differences.append({'path': new_path, 'type': 'added', 'value': json2[i]})
            elif i >= len2:
                differences.append({'path': new_path, 'type': 'removed', 'value': json1[i]})
            else:
                # Check if the values are different
                if json1[i] != json2[i]:
                    differences.append({'path': new_path, 'type': 'diff', 'value1': json1[i], 'value2': json2[i]})

    else:
        # Compare values directly if neither is a dict or list
        if json1 != json2:
            differences.append({'path': path, 'type': 'diff', 'value1': json1, 'value2': json2})

    return differences

# Highlighting function
def highlight_json(json_str, path, highlight_class):
    """Highlights the given path in the JSON string with the specified CSS class."""
    escaped_path = path.replace('.', r'\.').replace('[', r'\[').replace(']', r'\]')
    
    key_regex = r'("(' + escaped_path + r')":?)'
    value_regex = r'("(' + escaped_path + r')":?\s*(.*?))'

    json_str = re.sub(key_regex, r'<span class="' + highlight_class + r'">\1</span>', json_str)
    json_str = re.sub(value_regex, lambda m: m.group(0).replace(m.group(3), f'<span class="{highlight_class}">{m.group(3)}</span>'), json_str)

    return json_str

# AJAX view for JSON comparison
def compare_json_ajax(request):
    if request.method == "POST":
        json_obj1 = request.POST.get('json_obj1')
        json_obj2 = request.POST.get('json_obj2')

        try:
            dict1 = json.loads(json_obj1)
            dict2 = json.loads(json_obj2)

            differences = compare_json_objects(dict1, dict2)
            html_json1 = json.dumps(dict1, indent=4)
            html_json2 = json.dumps(dict2, indent=4)

            # Highlight differences in the JSON strings
            for diff in differences:
                path = diff['path']
                if diff['type'] == 'added':
                    html_json2 = highlight_json(html_json2, path, 'highlight-added')
                elif diff['type'] == 'removed':
                    html_json1 = highlight_json(html_json1, path, 'highlight-removed')
                elif diff['type'] == 'diff':
                    html_json1 = highlight_json(html_json1, path, 'highlight-diff')
                    html_json2 = highlight_json(html_json2, path, 'highlight-diff')

            return JsonResponse({'status': 'True', 'html_json1': html_json1, 'html_json2': html_json2})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'False', 'message': 'Invalid JSON provided.'})

    return JsonResponse({'status': 'False', 'message': 'Invalid request.'})
