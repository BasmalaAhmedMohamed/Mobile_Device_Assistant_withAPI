
system_prompt = '''
    <Role>
    {Role}
    </Role>
    <Format>
    {Format}
    </Format>
    <Task>
    {Task}
    </Task>
    <Context>
    {Context}
    </Context>
    '''



user_prompt= '''
    <external_data>
    The input from user:
    {text}
    The JSON must conform to the following schema:
    {schema}
    </external_data>
    '''

    