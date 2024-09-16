{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE OverloadedStrings #-}

import Data.Aeson
import qualified Data.ByteString.Char8 as BS
import qualified Data.Yaml as Y
import GHC.Generics
import System.Environment
import Plots
import qualified Data.Text as T
import qualified Data.Text.IO as T
import Data.Text (Text)
import Data.Maybe (fromMaybe)

data Contribution = Contribution
  { name :: Text,
    website :: Maybe Text,
    description :: Maybe Text,
    code :: [Text]
  } deriving (Show, Generic)

instance FromJSON Contribution

main :: IO ()
main = do
  let dataFile = "data/contributions.yaml"
--  let dataFile = "data/test.yaml"
  content <- BS.readFile dataFile 
  let parsedContent = Y.decodeEither content :: Either String [Contribution]
  case parsedContent of
    Left err -> error err
    Right xs -> do
        let allCode = mconcat (code <$> xs)
        print $ "Total number of contributions: " <> show (length allCode)
        print $ "Total number of NGI packages: " <> show (length xs - length nonNgiPackages)
        writeSvg "./out/channels.svg" $ Plots.channelPlot allCode
        writeSpec "./out/channels.vl" $ Plots.channelPlot allCode
        T.writeFile "./out/contributions.md" (makeBulletPoints xs)


nonNgiPackages = 
        ["Other", "Other Nix contributions", "Other nixpkgs contributions",
        "Flake templates", "2nix tools", "other flakes on ngi"]

makeBulletPoints :: [Contribution] -> Text
makeBulletPoints contributions = T.unlines (makeBulletPoint <$> contributions)

makeBulletPoint :: Contribution -> Text
makeBulletPoint contribution =
          "### " <> name contribution <> "\n\n" <>
          maybe  "" hrefLink (website contribution) <> "\n\n" <>
          fromMaybe "-" (description contribution) <> "\n\n" <>
                  T.unlines ((\x -> "- " <> hrefLink x) <$> code contribution)

        where hrefLink x = "[" <> T.take 69 x <> "](" <> x <> ")"
                

