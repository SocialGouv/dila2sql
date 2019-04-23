--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articles; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.articles (
    id text NOT NULL,
    section text,
    num text,
    titre text,
    etat text,
    date_debut date,
    date_fin date,
    type text,
    nota text,
    bloc_textuel text,
    dossier text,
    cid text NOT NULL,
    mtime integer NOT NULL
);


ALTER TABLE public.articles OWNER TO legipy;

--
-- Name: articles_calipsos; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.articles_calipsos (
    article_id text NOT NULL,
    calipso_id text NOT NULL
);


ALTER TABLE public.articles_calipsos OWNER TO legipy;

--
-- Name: calipsos; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.calipsos (
    id text NOT NULL
);


ALTER TABLE public.calipsos OWNER TO legipy;

--
-- Name: conteneurs; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.conteneurs (
    id text NOT NULL,
    titre text,
    etat text,
    nature text,
    num text,
    date_publi date,
    mtime integer NOT NULL
);


ALTER TABLE public.conteneurs OWNER TO legipy;

--
-- Name: db_meta; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.db_meta (
    key text NOT NULL,
    value text
);


ALTER TABLE public.db_meta OWNER TO legipy;

--
-- Name: duplicate_files; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.duplicate_files (
    id text NOT NULL,
    sous_dossier text NOT NULL,
    cid text,
    dossier text,
    mtime integer NOT NULL,
    data text NOT NULL,
    other_cid text,
    other_dossier text,
    other_mtime integer NOT NULL
);


ALTER TABLE public.duplicate_files OWNER TO legipy;

--
-- Name: liens; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.liens (
    src_id text NOT NULL,
    dst_cid text,
    dst_id text,
    dst_titre text,
    typelien text,
    _reversed boolean,
    CONSTRAINT liens_check CHECK (((length(dst_cid) > 0) OR (length(dst_id) > 0) OR (length(dst_titre) > 0)))
);


ALTER TABLE public.liens OWNER TO legipy;

--
-- Name: sections; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.sections (
    id text NOT NULL,
    titre_ta text,
    commentaire text,
    parent text,
    dossier text,
    cid text NOT NULL,
    mtime integer NOT NULL
);


ALTER TABLE public.sections OWNER TO legipy;

--
-- Name: sommaires; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.sommaires (
    cid text,
    parent text,
    element text NOT NULL,
    debut date,
    fin date,
    etat text,
    num text,
    "position" integer,
    _source text
);


ALTER TABLE public.sommaires OWNER TO legipy;

--
-- Name: tetiers; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.tetiers (
    id text NOT NULL,
    titre_tm text NOT NULL,
    niv integer NOT NULL,
    conteneur_id text NOT NULL
);


ALTER TABLE public.tetiers OWNER TO legipy;

--
-- Name: textes; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.textes (
    id integer NOT NULL,
    nature text NOT NULL,
    num text,
    nor text,
    titrefull_s text
);


ALTER TABLE public.textes OWNER TO legipy;

--
-- Name: textes_structs; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.textes_structs (
    id text NOT NULL,
    versions text,
    dossier text,
    cid text NOT NULL,
    mtime integer NOT NULL
);


ALTER TABLE public.textes_structs OWNER TO legipy;

--
-- Name: textes_versions; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.textes_versions (
    id text NOT NULL,
    nature text,
    titre text,
    titrefull text,
    titrefull_s text,
    etat text,
    date_debut date,
    date_fin date,
    autorite text,
    ministere text,
    num text,
    num_sequence integer,
    nor text,
    date_publi date,
    date_texte date,
    derniere_modification date,
    origine_publi text,
    page_deb_publi integer,
    page_fin_publi integer,
    visas text,
    signataires text,
    tp text,
    nota text,
    abro text,
    rect text,
    dossier text,
    cid text NOT NULL,
    mtime integer NOT NULL,
    texte_id integer
);


ALTER TABLE public.textes_versions OWNER TO legipy;

--
-- Name: textes_versions_brutes; Type: TABLE; Schema: public; Owner: legipy
--

CREATE TABLE public.textes_versions_brutes (
    id text NOT NULL,
    bits integer NOT NULL,
    nature text,
    titre text,
    titrefull text,
    autorite text,
    num text,
    date_texte date,
    dossier text,
    cid text NOT NULL,
    mtime integer NOT NULL
);


ALTER TABLE public.textes_versions_brutes OWNER TO legipy;

--
-- Name: textes_versions_brutes_view; Type: VIEW; Schema: public; Owner: legipy
--

CREATE VIEW public.textes_versions_brutes_view AS
 SELECT a.dossier,
    a.cid,
    a.id,
        CASE
            WHEN ((b.bits & 1) > 0) THEN b.nature
            ELSE a.nature
        END AS nature,
        CASE
            WHEN ((b.bits & 2) > 0) THEN b.titre
            ELSE a.titre
        END AS titre,
        CASE
            WHEN ((b.bits & 4) > 0) THEN b.titrefull
            ELSE a.titrefull
        END AS titrefull,
        CASE
            WHEN ((b.bits & 8) > 0) THEN b.autorite
            ELSE a.autorite
        END AS autorite,
        CASE
            WHEN ((b.bits & 16) > 0) THEN b.num
            ELSE a.num
        END AS num,
        CASE
            WHEN ((b.bits & 32) > 0) THEN b.date_texte
            ELSE a.date_texte
        END AS date_texte,
    a.titrefull_s
   FROM (public.textes_versions a
     LEFT JOIN public.textes_versions_brutes b ON (((b.id = a.id) AND (b.cid = a.cid) AND (b.dossier = a.dossier) AND (b.mtime = a.mtime))));


ALTER TABLE public.textes_versions_brutes_view OWNER TO legipy;

--
-- Name: articles articles_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_id_key UNIQUE (id);


--
-- Name: calipsos calipsos_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.calipsos
    ADD CONSTRAINT calipsos_id_key UNIQUE (id);


--
-- Name: conteneurs conteneurs_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.conteneurs
    ADD CONSTRAINT conteneurs_id_key UNIQUE (id);


--
-- Name: db_meta db_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.db_meta
    ADD CONSTRAINT db_meta_pkey PRIMARY KEY (key);


--
-- Name: duplicate_files duplicate_files_id_sous_dossier_cid_dossier_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.duplicate_files
    ADD CONSTRAINT duplicate_files_id_sous_dossier_cid_dossier_key UNIQUE (id, sous_dossier, cid, dossier);


--
-- Name: sections sections_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.sections
    ADD CONSTRAINT sections_id_key UNIQUE (id);


--
-- Name: tetiers tetiers_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.tetiers
    ADD CONSTRAINT tetiers_id_key UNIQUE (id);


--
-- Name: textes textes_nature_num_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes
    ADD CONSTRAINT textes_nature_num_key UNIQUE (nature, num);


--
-- Name: textes textes_nor_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes
    ADD CONSTRAINT textes_nor_key UNIQUE (nor);


--
-- Name: textes textes_pkey; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes
    ADD CONSTRAINT textes_pkey PRIMARY KEY (id);


--
-- Name: textes_structs textes_structs_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes_structs
    ADD CONSTRAINT textes_structs_id_key UNIQUE (id);


--
-- Name: textes textes_titrefull_s_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes
    ADD CONSTRAINT textes_titrefull_s_key UNIQUE (titrefull_s);


--
-- Name: textes_versions_brutes textes_versions_brutes_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes_versions_brutes
    ADD CONSTRAINT textes_versions_brutes_id_key UNIQUE (id);


--
-- Name: textes_versions textes_versions_id_key; Type: CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes_versions
    ADD CONSTRAINT textes_versions_id_key UNIQUE (id);


--
-- Name: article_calipsos_double_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE UNIQUE INDEX article_calipsos_double_idx ON public.articles_calipsos USING btree (article_id, calipso_id);


--
-- Name: calipsos_id_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX calipsos_id_idx ON public.calipsos USING btree (id);


--
-- Name: conteneurs_id_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX conteneurs_id_idx ON public.conteneurs USING btree (id);


--
-- Name: conteneurs_num_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX conteneurs_num_idx ON public.conteneurs USING btree (num);


--
-- Name: liens_dst_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX liens_dst_idx ON public.liens USING btree (dst_id) WHERE _reversed;


--
-- Name: liens_src_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX liens_src_idx ON public.liens USING btree (src_id) WHERE (NOT _reversed);


--
-- Name: sommaires_parent_debut_fin_etat_num_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX sommaires_parent_debut_fin_etat_num_idx ON public.sommaires USING btree (parent, debut, fin, etat, num);


--
-- Name: sommaires_source_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX sommaires_source_idx ON public.sommaires USING btree (_source);


--
-- Name: tetiers_id_idx; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX tetiers_id_idx ON public.tetiers USING btree (id);


--
-- Name: textes_versions_texte_id; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX textes_versions_texte_id ON public.textes_versions USING btree (texte_id);


--
-- Name: textes_versions_titrefull_s; Type: INDEX; Schema: public; Owner: legipy
--

CREATE INDEX textes_versions_titrefull_s ON public.textes_versions USING btree (titrefull_s);


--
-- Name: textes_versions textes_versions_texte_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: legipy
--

ALTER TABLE ONLY public.textes_versions
    ADD CONSTRAINT textes_versions_texte_id_fkey FOREIGN KEY (texte_id) REFERENCES public.textes(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: adipasquale
--

GRANT ALL ON SCHEMA public TO legipy;


--
-- PostgreSQL database dump complete
--

