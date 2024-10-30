from notion_connector.notion_handler import NotionHandler

# Tests
notion_handler = NotionHandler()

projects = notion_handler.read_projects()
