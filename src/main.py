from file_generator import clear_and_copy_files, generate_pages_recursive


def main():
    # type = TextType.TEXT

    # t =TextNode(
    #     text = "Hello, world!", 
    #     text_type = type, 
    #     url = "https://example.com"
    #     )
    # print(t)
    clear_and_copy_files('static', 'public')
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="public"
    )
if __name__ == "__main__":
    main()