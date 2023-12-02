module Main (main) where
import Lib
import System.IO
import System.Environment (getArgs)

import qualified Day02
latest :: String
latest = "02"
every :: [String]
every = ["02"]


headerDispatch :: String -> InputType -> IO ()
headerDispatch day input = do
  putStrLn $ "==== Day " ++ day ++ " ===="
  dispatch day input
  putStrLn "\n"

dispatch :: String -> InputType -> IO()
dispatch day input = getRunner day $ getInput day input

getRunner :: String -> IO String -> IO ()
getRunner day = case day of 
  "02"   -> Day02.run
  n     -> \_ -> putStrLn ("Solution Unavailable For Day " ++ n)

getType :: [String] -> InputType
getType x = case x of
  "-t1":_ -> Test1
  "-t2":_ -> Test2
  _:xs    -> getType xs
  _       -> Input

getDay :: [String] -> IO String
getDay x = case x of
  "-i":_ -> putStr "Select Day: " >> hFlush stdout >> (pad <$> getLine)
  "-a":_ -> return "all"
  _:xs   -> getDay xs
  _      -> return latest

main :: IO ()
main = do
  args <- getArgs
  day <- getDay args
  let input = getType args
  if day == "all" then foldMap headerDispatch every input else dispatch day input