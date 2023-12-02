module Lib
    ( getInput
    , split
    , InputType(..)
    , pad
    ) where


split :: Char -> String -> [String]
split c str = case break (== c) str of
  (a, _comma:xs) -> a : split c xs
  ("", _) -> []
  (a, _) -> [a]


data InputType = Test1 | Test2 | Input

pad :: String -> String
pad s = if length s < 2 then "0" ++ s else s

getFilePath :: String -> InputType -> String
getFilePath day i = "../inputs/" ++ pad day ++ "/" ++ case i of
  Test1 -> "test1.txt"
  Test2 -> "test2.txt"
  Input -> "input.txt"

getInput :: String -> InputType -> IO String
getInput day i = readFile $ getFilePath day i