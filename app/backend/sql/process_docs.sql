-- Match files by name only: delete a file's rows from docs_chunks_table first to reprocess a re-uploaded PDF
INSERT INTO docs_chunks_table (file_name, chunk, chunk_index)
SELECT
  d.relative_path AS file_name,
  c.value::VARCHAR AS chunk,
  c.index AS chunk_index
FROM DIRECTORY(@raw_docs_stage) AS d,
  LATERAL FLATTEN(
    input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
      SNOWFLAKE.CORTEX.PARSE_DOCUMENT(@raw_docs_stage, d.relative_path, {'mode': 'LAYOUT'}):content::VARCHAR,
      'markdown',
      1500,
      200
    )
  ) AS c
WHERE d.relative_path NOT IN (SELECT DISTINCT file_name FROM docs_chunks_table WHERE file_name IS NOT NULL)
